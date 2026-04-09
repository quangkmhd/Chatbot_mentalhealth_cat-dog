import json
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from src.chat_bot.utils.logging import app_logger
from src.chat_bot.config import settings

class PetMartCrawler:
    def __init__(self, storage_dir=settings.RAW_DATA_DIR):
        self.storage_dir = storage_dir
        self.crawled_links_file = os.path.join(storage_dir, "crawled_links.json")
        self.crawled_links = set()
        
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
            
        self._load_crawled_links()

    def _load_crawled_links(self):
        if os.path.exists(self.crawled_links_file):
            try:
                with open(self.crawled_links_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.crawled_links = set(data.get("crawled_links", []))
                app_logger.info(f"Loaded {len(self.crawled_links)} already crawled links.")
            except Exception as e:
                app_logger.error(f"Error loading crawled links: {e}")

    def _save_crawled_links(self):
        try:
            with open(self.crawled_links_file, 'w', encoding='utf-8') as f:
                json.dump({"crawled_links": list(self.crawled_links)}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            app_logger.error(f"Error saving crawled links: {e}")

    def _generate_filename(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path.strip('/')
        if not path:
            path = "index"
        else:
            path = path.replace('/', '_')
        return f"{path}.json"

    def crawl_url(self, url, delay=1):
        if url in self.crawled_links:
            app_logger.info(f"Already crawled: {url}")
            return False
        
        try:
            app_logger.info(f"Crawling: {url}")
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                app_logger.warning(f"Failed to access {url} - Status: {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text_content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            title = soup.title.get_text() if soup.title else "No Title"
            
            data = {
                "url": url,
                "title": title,
                "crawled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content": text_content
            }
            
            filename = self._generate_filename(url)
            filepath = os.path.join(self.storage_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.crawled_links.add(url)
            app_logger.info(f"Successfully crawled: {url}")
            time.sleep(delay)
            return True
            
        except Exception as e:
            app_logger.error(f"Error crawling {url}: {e}")
            return False

    def crawl_from_list(self, links, delay=1):
        app_logger.info(f"Starting crawl for {len(links)} links")
        for i, link in enumerate(links, 1):
            self.crawl_url(link, delay)
            if i % 10 == 0:
                self._save_crawled_links()
        self._save_crawled_links()
