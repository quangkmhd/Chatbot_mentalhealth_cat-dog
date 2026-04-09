# Architecture Deep Dive: PawsitiveMind Mental Health Chatbot

## 1. System Overview

PawsitiveMind is an end-to-end Retrieval-Augmented Generation (RAG) ecosystem focused specifically on providing empathetic, therapeutic conversational AI. To achieve high relevancy and reduce the risk of harmful AI hallucinations in a medical context, the system relies heavily on a tightly controlled, highly curated vector database rather than the pre-trained knowledge of the LLM alone.

The architecture is split into two distinct phases: an **Offline Data Pipeline** (for scraping, cleaning, and embedding clinical literature) and an **Online Chat Interface** (for real-time retrieval and generation).

## 2. Core Architectural Components

### 2.1. The Data Ingestion Pipeline (`2-crawler.py` & `1-extraction.py`)
- **Web Crawler:** Built using `requests` and `BeautifulSoup4`. It recursively crawls trusted psychological resources, forum Q&As, and cognitive behavioral therapy (CBT) manuals. It is designed to respect `robots.txt` and uses exponential backoff to prevent overwhelming source servers.
- **Text Cleansing:** The raw HTML is stripped. The extraction script uses regex to remove navigation bars, ads, and irrelevant UI text, resulting in a pure JSON structure of `{ "topic": "...", "content": "..." }`.

### 2.2. The Embedding & Vector Store (`3-embedding.py`)
- **Text Splitting:** Uses LangChain's `RecursiveCharacterTextSplitter`. Because psychological context often relies on the flow of a paragraph, chunks are kept relatively large (e.g., 1000 tokens) with significant overlap.
- **Embedding Model:** Utilizes `SentenceTransformers`. By default, a fast, dense model like `all-MiniLM-L6-v2` is used to map the emotional and semantic meaning of text into a 384-dimensional space.
- **LanceDB:** The chosen vector database. Unlike heavy client-server DBs (like Milvus or Pinecone), LanceDB operates entirely locally (serverless) on top of the Lance columnar data format. This provides Blazing fast vector search directly from the local disk without managing a separate database process.

### 2.3. The LLM Engine (Groq / `4-chat.py`)
- **Groq LPU Processing:** Mental health chatbots require immediate responses to maintain conversational flow. PawsitiveMind utilizes the Groq API, which runs on specialized Language Processing Units (LPUs), achieving token generation speeds often exceeding 500 tokens/second.
- **Prompt Engineering:** The retrieved context from LanceDB is injected into a strict `system_prompt.py`. The prompt mathematically instructs the model to act as an empathetic listener, never diagnose, and base its advice *only* on the provided context.

### 2.4. The Web Frontend (`app.py`)
- **Flask Server:** A lightweight synchronous server that hosts the UI and exposes a `/chat` API endpoint.
- **Session Memory:** Uses simple server-side data structures or LangChain `ConversationBufferMemory` to remember the last 5-10 exchanges. This ensures that if a user says "I tried what you suggested," the bot knows what the suggestion was.

## 3. Data Flow Diagram

**Phase 1: Knowledge Base Generation (Offline)**
1. `2-crawler.py` -> Fetches HTML -> Saves raw data.
2. `1-extraction.py` -> Cleans text -> `plain_links.json`.
3. `3-embedding.py` -> SentenceTransformer encodes text -> Saves to LanceDB directory (`./data/lancedb`).

**Phase 2: Conversation (Online)**
1. User types a message in the Web UI.
2. Flask POSTs message to the backend logic.
3. The message is embedded using the exact same SentenceTransformer model.
4. The system queries LanceDB for the top 4 most semantically similar paragraphs.
5. The retrieved text + chat history + user message are combined via LangChain prompt templates.
6. The combined prompt is sent via API to Groq (running Llama-3 or Mixtral).
7. Groq returns the empathetic response, which is streamed back to the Web UI.

## 4. Design Decisions & Trade-offs

- **LanceDB vs. Pinecone:** A local, file-based database (LanceDB) was chosen over a managed cloud service (Pinecone) to ensure complete data privacy and eliminate network latency during the retrieval step.
- **Groq API vs. Local LLM:** While Askly (another RAG tool) uses local Hugging Face models, PawsitiveMind prioritizes emotional intelligence and speed. Extremely large models (like Llama-3 70B) provide much better empathy than 7B models. Since running a 70B model locally requires multiple expensive GPUs, routing this to Groq is far more practical and lightning-fast.
- **Safety Constraints:** The architecture relies on the `system_prompt.py` as a hard safeguard to prevent the bot from acting as a licensed medical professional, pushing it instead toward active listening and established coping mechanisms.
