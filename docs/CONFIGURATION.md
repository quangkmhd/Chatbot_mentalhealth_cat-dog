# Configuration Guide

All system settings are centralized in `src/chat_bot/config.py` using Pydantic's `BaseSettings`. This allows for validation and easy overrides via environment variables.

## Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | API Key for Groq Cloud | Required |
| `OPENROUTER_API_KEY` | API Key for OpenRouter | Optional |
| `SECRET_KEY` | Flask session secret key | dev-secret |

## Model Settings

- **Embedding Model**: `intfloat/multilingual-e5-large` (1024 dims)
- **Primary LLM**: `llama-3.3-70b-versatile` (Groq)
- **Secondary LLM**: `deepseek/deepseek-chat-v3-0324:free` (OpenRouter)

## Path Settings

- **Data Directory**: `./data`
- **Vector DB**: `./data/lancedb_clean`
- **Logs**: `./data/logs`
- **Raw Data**: `./petmart_data`

## Adjusting Search
In `config.py`, change `NUM_SEARCH_RESULTS` to control how many context chunks are retrieved for each query.
