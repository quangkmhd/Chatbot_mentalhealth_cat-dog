import requests
from bs4 import BeautifulSoup
import time
import os
import json
from tqdm import tqdm
from src.chat_bot.utils.logging import app_logger
from src.chat_bot.config import settings

def get_plain_links(base_url, num_pages=50, existing_links=None):
    if existing_links is None:
        existing_links = []
    
    all_plain_links = []
    
    for page in tqdm(range(1, num_pages + 1), desc="Fetching links"):
        url = base_url if page == 1 else f"{base_url}/page/{page}"
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            plain_links = soup.find_all('a', class_='plain')
            
            for link in plain_links:
                if 'href' in link.attrs:
                    link_url = link['href']
                    if link_url not in existing_links and link_url not in all_plain_links:
                        all_plain_links.append(link_url)
            
            time.sleep(1)
        except Exception as e:
            app_logger.error(f"Error processing page {url}: {e}")
            break
            
    return all_plain_links

def main():
    base_url = "https://www.petmart.vn/cho-canh"
    links_file = os.path.join(settings.BASE_DIR, "plain_links.json")
    
    existing_data = {}
    if os.path.exists(links_file):
        with open(links_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            
    existing_links = existing_data.get("links", [])
    app_logger.info(f"Loaded {len(existing_links)} existing links.")
    
    new_links = get_plain_links(base_url, num_pages=10) # Limited for demo
    all_links = list(set(existing_links + new_links))
    
    result = {
        "source": base_url,
        "total_links": len(all_links),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "links": all_links
    }
    
    with open(links_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
        
    app_logger.info(f"Saved {len(all_links)} links to {links_file}")

if __name__ == "__main__":
    main()
