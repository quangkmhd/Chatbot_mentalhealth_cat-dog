# API & Script Reference: PawsitiveMind Chatbot

This document provides documentation for the Python scripts forming the ingestion pipeline and the web API endpoints.

## 1. Management Scripts (`src/scripts/`)

### `crawl_links.py`
Scrapes PetMart to discover relevant article links.

**Execution:**
```bash
python -m src.scripts.crawl_links
```

### `ingest_data.py`
The master ingestion pipeline.

**Execution:**
```bash
python -m src.scripts.ingest_data [--crawl]
```
**Behavior:**
1. (Optional) Crawls full article content for the discovered links.
2. Cleans text and splits it into manageable tokens (512 tokens).
3. Encodes texts via `intfloat/multilingual-e5-large`.
4. Stores vectors and metadata in LanceDB (`data/lancedb_clean`).

## 2. Core Modules (`src/chat_bot/`)

### `models/vector_db.py`
Handles all interactions with the LanceDB vector store.
- `get_embedding(text)`: Returns a 1024-dim vector.
- `search(query, limit)`: Performs semantic search and returns formatted context.
- `add_chunks(chunks)`: Adds new data to the index.

### `core/chat_logic.py`
Orchestrates the LLM interaction.
- `ChatManager.get_response(messages, context, model_choice)`: Formats the prompt and calls Groq or OpenRouter.
- Handles system prompt templates and reasoning strategies (CoT, ReAct).

## 3. Web API (`src/chat_bot/api/app.py`)

The Flask application serves as the primary user interface.

### `POST /chat`
Receives user input and returns the assistant's response.

**Request Body:**
```json
{
  "message": "My pet is acting strange.",
  "history": [{"role": "user", "content": "Hello"}]
}
```

**Response:**
```json
{
  "response": "...",
  "context": "Retrieved data used for this response"
}
```

## 4. Dashboard (`src/chat_bot/api/dashboard.py`)
A Streamlit-based diagnostic tool for internal testing and data verification.
Run via: `streamlit run src/chat_bot/api/dashboard.py`
