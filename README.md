# PawsitiveMind - Mental Health Chatbot

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![LanceDB](https://img.shields.io/badge/LanceDB-Vector_DB-orange?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Powered-F55036?style=flat-square)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-yellow.svg?style=flat-square)

Provide empathetic, 24/7 mental health support using an intelligent Retrieval-Augmented Generation (RAG) chatbot. Designed for wellness platforms, counseling centers, and health tech developers, PawsitiveMind leverages LanceDB and the lightning-fast Groq API to deliver sub-second, contextually accurate responses grounded in a vast library of therapeutic dialogues.

![PawsitiveMind Chatbot Demo](assets/demo.png)

## ✨ Key Features

- **Efficient Data Ingestion**: Extract and embed therapeutic dialogues using `src.scripts.ingest_data` into LanceDB's serverless vector store.
- **Ultra-low Latency**: Integrated with Groq API for lightning-fast response generation using Llama-3.3-70b.
- **Modular Design**: Separated concerns into `core`, `models`, `services`, and `api` modules for maximum maintainability.
- **Multiple Interfaces**: Choose between a Flask-based web UI and a Streamlit-based dashboard.
- **Scalable Retrieval**: Advanced RAG pipeline with customizable chunking and overlap in the `models/vector_db.py`.
- **Flexible LLM Support**: Drop-in support for Groq and OpenRouter (DeepSeek) via `core/chat_logic.py`.

## 🚀 Quick Start

Get your compassionate chatbot running in under 5 minutes.

```bash
# 1. Clone the repository
git clone https://github.com/quangkmhd/Chatbot_mentalhealth_cat-dog.git
cd Chatbot_mentalhealth_cat-dog

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (.env)
GROQ_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
SECRET_KEY=your_flask_secret

# 4. Start the Flask chat interface
python main.py
```

**Expected Output:**
```text
 * Serving Flask app 'src.chat_bot.api.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```
Open your browser to `http://127.0.0.1:5000` to start chatting with the mental health assistant.

## 📦 Installation

Ideal for local testing and modification.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 💻 Usage Examples

### Example 1: Scraping and Ingesting Data

**Problem:** You need to build a specialized knowledge base from curated mental health resources.

```bash
# Fetch links from source
python -m src.scripts.crawl_links

# Run the full ingestion pipeline (crawl articles -> chunk -> embed -> store)
python -m src.scripts.ingest_data --crawl
```
**Expected Output:** A structured LanceDB dataset in `data/vector_db` populated with clean, usable text documents ready for semantic search.

### Example 2: Generating the Vector Database (Code Level)

**Problem:** You want to programmatically interact with the vector store.

```python
from src.chat_bot.models.vector_db import VectorDBManager

# Initialize Manager
db_manager = VectorDBManager()

# Search for relevant context
context = db_manager.search("How to deal with work stress?")
print(context)
```
*Concept: `VectorDBManager` abstracts away the complexity of embedding generation and LanceDB queries.*

### Example 3: Running the Streamlit Dashboard

**Problem:** You want an interactive, data-rich interface for testing and monitoring.

```bash
# Start the Streamlit dashboard
streamlit run src/chat_bot/api/dashboard.py
```
*Concept: The dashboard provides a visual way to see retrieved context and model thought processes in real-time.*

## 🔧 Troubleshooting

- **Groq API Rate Limits (HTTP 429):**
  - *Cause:* Sending too many requests per minute on the free tier.
  - *Solution:* Implement an exponential backoff in `4-chat.py` or upgrade your Groq API plan.
- **LanceDB Connection Issues:**
  - *Cause:* Corrupted database files or missing write permissions in the `./data` directory.
  - *Solution:* Delete the `./data/lancedb` folder and re-run `3-embedding.py` to rebuild the index from scratch.
- **BeautifulSoup Crawler Blocking:**
  - *Cause:* Target websites blocking Python's default user-agent during `2-crawler.py` execution.
  - *Solution:* Add a randomized User-Agent header in the `requests.get()` call within the crawler script.

## 📚 Documentation Links

- **[System Prompt Engineering](./docs/SYSTEM_PROMPT.md)**  
  Delve into the precise prompt architecture that gives the chatbot its compassionate, empathetic persona. Explore how specific instructions guide the LLM to process retrieved therapeutic context, ensuring responses are consistently safe, supportive, and perfectly tuned for mental wellness.

- **[Integrating OpenAI Models](./docs/OPENAI_SETUP.md)**  
  Learn how to seamlessly switch from Groq to OpenAI's powerful GPT models for enhanced reasoning. This guide walks you through the exact environment configurations and API payload adjustments required to upgrade your chatbot's conversational capabilities.

- **[Deploying to Heroku/Render](./docs/DEPLOYMENT.md)**  
  Take your mental health assistant from local development to a globally accessible production environment. Discover step-by-step instructions for containerizing the Flask app, configuring persistent LanceDB storage, and managing secure environment variables in the cloud.

## 🤝 Contributing

We are passionate about using AI for mental health and welcome your contributions!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/better-empathy-prompts`
3. Commit your changes: `git commit -m 'Improve system prompt for anxiety topics'`
4. Push to the branch: `git push origin feature/better-empathy-prompts`
5. Open a Pull Request.

Please ensure your changes align with ethical guidelines regarding AI-generated health advice.

## 📄 License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for full text.

## 🙏 Credits

- UI inspiration from modern chat platforms.
- Vector search powered by [LanceDB](https://lancedb.com/).
- LLM inference accelerated by [Groq](https://groq.com/).
