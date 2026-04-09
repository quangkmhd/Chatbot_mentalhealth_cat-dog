import os
import json
import glob
from tqdm import tqdm
from src.chat_bot.config import settings
from src.chat_bot.services.crawler import PetMartCrawler
from src.chat_bot.models.vector_db import VectorDBManager
from src.chat_bot.utils.logging import app_logger

def run_ingestion(crawl=False):
    """Run the full data ingestion pipeline."""
    
    # 1. Crawl if requested
    if crawl:
        links_file = os.path.join(settings.BASE_DIR, "plain_links.json")
        if os.path.exists(links_file):
            with open(links_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            links = data.get("links", [])
            crawler = PetMartCrawler()
            crawler.crawl_from_list(links)
        else:
            app_logger.error(f"Links file not found: {links_file}")
            return

    # 2. Embedding & DB Ingestion
    db_manager = VectorDBManager()
    db_manager.create_table() # Overwrites existing data
    
    json_files = glob.glob(os.path.join(settings.RAW_DATA_DIR, "*.json"))
    app_logger.info(f"Processing {len(json_files)} files for embedding...")
    
    all_chunks = []
    
    for json_file in tqdm(json_files, desc="Chunking files"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            filename = os.path.basename(json_file)
            title = data.get("title", "")
            content = "\n".join(data.get("content", []))
            
            if len(content) < 50:
                continue
                
            # Use local chunking logic (simplified)
            from transformers import AutoTokenizer
            tokenizer = db_manager.tokenizer
            tokens = tokenizer.encode(content, add_special_tokens=False)
            
            max_tokens = 512
            overlap = 50
            
            for i in range(0, len(tokens), max_tokens - overlap):
                chunk_tokens = tokens[i:i + max_tokens]
                if len(chunk_tokens) < 50: continue
                
                chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
                all_chunks.append({
                    "text": chunk_text,
                    "metadata": {"filename": filename, "title": title}
                })
        except Exception as e:
            app_logger.error(f"Error processing {json_file}: {e}")

    # Process embeddings in batches via the manager
    app_logger.info(f"Adding {len(all_chunks)} chunks to LanceDB...")
    db_manager.add_chunks(all_chunks)
    
    app_logger.info("Ingestion complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--crawl", action="store_true", help="Run crawler before embedding")
    args = parser.parse_args()
    
    run_ingestion(crawl=args.crawl)
