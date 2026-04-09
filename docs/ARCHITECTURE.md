# Architecture Deep Dive: PawsitiveMind Mental Health Chatbot

## 1. System Overview

PawsitiveMind is an end-to-end Retrieval-Augmented Generation (RAG) ecosystem focused specifically on providing empathetic, therapeutic conversational AI. To achieve high relevancy and reduce the risk of harmful AI hallucinations, the system relies on a tightly controlled, highly curated vector database.

The architecture is split into two distinct phases: an **Offline Data Pipeline** (for scraping, cleaning, and embedding) and an **Online Chat Interface** (for real-time retrieval and generation).

## 2. Core Architectural Components

### 2.1. The Data Ingestion Pipeline (`src/scripts/`)
- **Web Crawler (`src/chat_bot/services/crawler.py`):** Built using `requests` and `BeautifulSoup4`. It recursively crawls trusted resources. It is designed to respect server limits and uses delays to prevent overlapping requests.
- **Ingestion Script (`src/scripts/ingest_data.py`):** Orchestrates the raw data processing, chunking, and storage into the vector database.

### 2.2. The Embedding & Vector Store (`src/chat_bot/models/vector_db.py`)
- **Text Splitting:** Uses `transformers` tokenizer-based splitting to ensure chunks stay within model context limits (512 tokens) with overlap (50 tokens).
- **Embedding Model:** Utilizes `intfloat/multilingual-e5-large`. This 1024-dimensional model provides superior performance for both English and Vietnamese text.
- **LanceDB:** Operates entirely locally (serverless) on top of the Lance columnar data format. This provides blazing fast vector search directly from the local disk.

### 2.3. The LLM Engine (`src/chat_bot/core/chat_logic.py`)
- **Groq LPU Processing:** Utilizes the Groq API (Llama-3.3-70b-versatile) for rapid token generation.
- **Prompt Engineering:** The retrieved context from LanceDB is injected into a comprehensive system prompt designed for empathetic veterinary/health assistance.

### 2.4. The Presentation Layer (`src/chat_bot/api/`)
- **Flask Server (`app.py`):** Provides a full-featured web interface with session-based chat history.
- **Streamlit Dashboard (`dashboard.py`):** A secondary interface for developers to test and monitor the RAG output and context retrieval.

## 3. Data Flow Diagram

**Phase 1: Knowledge Base Generation (Offline)**
1. `src/scripts/crawl_links.py` -> Gathers URLs.
2. `src/scripts/ingest_data.py` ->
   - Calls `PetMartCrawler` to save raw JSON.
   - Chunks text.
   - Calls `VectorDBManager` to encode and save to `data/lancedb_clean`.

**Phase 2: Conversation (Online)**
1. User types a message in the Web UI.
2. `src/chat_bot/api/app.py` receives the POST request.
3. `VectorDBManager` embeds the query and searches LanceDB.
4. `ChatManager` combines context + history + message.
5. Combined prompt is sent to Groq or OpenRouter.
6. Response is returned and saved to the session.

## 4. Design Decisions & Trade-offs

- **Multilingual-E5-Large:** Chosen for its excellent performance in Vietnamese, which is critical for the target user base.
- **Modular Packaging:** Moving from flat scripts to a proper Python package (`src/chat_bot`) allows for better testing and reuse of components.
- **Pydantic Configuration:** Centralizing all settings in `config.py` ensures that changes to model names or database paths are reflected everywhere instantly.
