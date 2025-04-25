<<<<<<< HEAD
# Pet Health Assistant Project

## Overview
This project creates a veterinary assistant chatbot that helps pet owners with health concerns. It uses web crawling to collect pet health data (a trusted Vietnamese pet care resource), vector embeddings for semantic search, and large language model integration for intelligent responses.

<div align="center">
  <img src="static\images\web.png" alt="Pet Health Assistant" width="800"/>
</div>

## Features
- Data collection through web crawling from web
- Vietnamese-focused pet health knowledge base
- Vector database for semantic search
- AI-powered conversation with veterinary knowledge
- Multiple LLM backend options 

## System Architecture

```
┌─────────────┐    ┌───────────────┐    ┌────────────────┐    ┌────────────┐
│ Web Crawler │───►│ Content Parser │───►│ Text Embedding │───►│  LanceDB   │
│ (petmart.vn)│    └───────────────┘    └────────────────┘    └────────┬───┘
└─────────────┘                                                        │
                                                                       │
┌──────────────────────────────────────────────────────────────────────┘
│
▼
┌────────────────┐    ┌──────────────┐    ┌───────────────┐
│  User Question │───►│ Flask Server │◄───┤ LLM (Groq or  │
│                │    │              │    │  OpenRouter)  │
└────────────────┘    └──────────────┘    └───────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │   Response   │
                      └──────────────┘
```

## Project Components

### 1. Data Collection (`1-extraction.py`)
- Web crawler that extracts 
- Focuses on the pet health and veterinary sections
- Stores links in JSON format for further processing
- Handles pagination and implements rate limiting

### 2. Content Extraction (`2-crawler.py`)
- `FirecrawlApp` class for structured content extraction
- Processes links collected in the previous step
- Saves crawled data with metadata
- Implements logging and error handling

### 3. Vector Database Creation (`3-embedding.py`)
- Text chunking for better search results
- Embedding generation using `multilingual-e5-large` model 
- LanceDB integration for efficient vector storage
- Progress tracking using tqdm

### 4. Web Application (`app.py`)
- Flask web application with responsive UI
- Integration with Groq and OpenRouter APIs
- Context-aware responses using vector similarity search
- Session management for conversation history

## Data Flow

1. **Data Collection Phase**:
   - Web crawler extracts pet health information web
   - Content is parsed and cleaned
   - Text is split into manageable chunks

2. **Embedding Phase**:
   - Text chunks are converted to vector embeddings
   - Embeddings are stored in LanceDB

3. **Query Phase**:
   - User asks a question about pet health
   - Question is converted to vector embedding
   - Similar vectors are retrieved from database
   - Context is sent to LLM with user query
   - LLM generates a veterinary-knowledge based response

## Setup Instructions

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pet-health-assistant
```

2. Create and activate a virtual environment:
=======
