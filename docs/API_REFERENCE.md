# API & Script Reference: PawsitiveMind Chatbot

This document provides documentation for the Python scripts forming the ingestion pipeline and the web API endpoints for the chatbot interface.

## 1. The Offline Data Pipeline

### `2-crawler.py`
Scrapes data from mental health resources.

**Execution:**
```bash
python 2-crawler.py --urls "https://example.com/cbt-guide" --depth 2
```
**Key Functions:**
- `fetch_page(url)`: Handles HTTP requests with appropriate headers to avoid 403 blocks.
- `extract_links(html, base_url)`: Discovers child links up to the specified `--depth`.

### `1-extraction.py`
Processes raw HTML/text dumps into clean, embeddable JSON.

**Execution:**
```bash
python 1-extraction.py --input ./raw_data --output plain_links.json
```
**Output Format (`plain_links.json`):**
```json
[
  {
    "id": "doc_001",
    "title": "Managing Panic Attacks",
    "text": "A panic attack is a sudden episode of intense fear..."
  }
]
```

### `3-embedding.py`
Creates the LanceDB vector index.

**Execution:**
```bash
python 3-embedding.py
```
**Behavior:**
1. Loads `plain_links.json`.
2. Splits long texts using LangChain splitters.
3. Encodes texts via Hugging Face.
4. Commits data to `./data/lancedb/therapy_docs.lance`.

## 2. Flask Web API (`app.py`)

The Flask application serves the static HTML/CSS files and provides an endpoint for chat interaction.

### `POST /api/chat`
The main endpoint that receives user input and returns the LLM response.

**Request Body:**
```json
{
  "message": "I've been feeling really down today.",
  "session_id": "usr_98765"
}
```
*Note: `session_id` is used to maintain conversation history in memory.*

**Response (JSON):**
```json
{
  "response": "I'm so sorry to hear that you're having a tough day. It's completely valid to feel down sometimes. Based on the cognitive behavioral resources I have, it can sometimes help to... Would you like to talk more about what's making you feel this way?",
  "sources_used": ["Managing Depression Guide", "CBT Techniques"]
}
```

## 3. Core Chat Logic (`4-chat.py`)

This script can be run standalone as a CLI chatbot or imported as a module by `app.py`.

### `class TherapyBot`

#### `__init__(self, db_path: str = "./data/lancedb")`
Initializes the LanceDB connection and sets up the LangChain LLM chain using the Groq API client.

#### `retrieve_context(self, query: str, k: int = 3) -> str`
Embeds the user query and searches the LanceDB table. Returns a concatenated string of the most relevant therapeutic texts.

#### `get_response(self, user_input: str) -> str`
1. Calls `retrieve_context`.
2. Formats the `system_prompt.py` with the context and the user's input.
3. Executes the API call to Groq.
4. Appends the interaction to the local memory buffer.
5. Returns the generated string.
