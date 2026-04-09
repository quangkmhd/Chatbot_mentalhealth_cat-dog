# Configuration Guide: PawsitiveMind Chatbot

This document covers all environment variables, LLM parameters, and prompt configurations required to tune the mental health chatbot.

## 1. Environment Variables (`.env`)

The system relies on external APIs for inference. Ensure your `.env` file is properly populated.

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Authentication key for the Groq LPU inference engine. | **Yes** | `gsk_abc123...` |
| `OPENAI_API_KEY` | Optional fallback. If set, you can configure LangChain to use GPT-4o instead of Groq. | No | `sk-proj-...` |
| `FLASK_ENV` | Sets Flask to development (debug on) or production. | No | `development` |
| `LANCEDB_PATH` | Directory where the vector database files are stored. | No | `./data/lancedb` |

## 2. LLM Model Selection & Hyperparameters

Configured within `4-chat.py` (or wherever the LangChain ChatModel is initialized).

### Groq Model Selection
Because mental health conversations require high reasoning capabilities and emotional intelligence, larger models are strictly recommended.
- **Recommended Model:** `llama3-70b-8192` (Llama 3 70-Billion parameter). Offers excellent nuance and following of safety instructions.
- **Alternative:** `mixtral-8x7b-32768`. Excellent for handling extremely long conversation histories due to its 32k context window.

### Hyperparameters
- **`temperature`:** `0.4` to `0.6`. A purely deterministic model (`0.0`) sounds robotic and cold. A slight temperature allows the model to vary its phrasing and sound more empathetic and human-like without hallucinating facts.
- **`max_tokens`:** `300`. Responses should be conversational and digestible. If the bot outputs 1000-word essays, the user will feel overwhelmed.

## 3. System Prompt Engineering (`system_prompt.py`)

This is the most critical configuration file in the project. It dictates the persona, safety boundaries, and operating rules of the AI.

**Example Configuration inside `system_prompt.py`:**
```python
SYSTEM_PROMPT = """
You are PawsitiveMind, a highly empathetic, warm, and non-judgmental mental health companion.
Your primary goal is active listening and validation.

CRITICAL RULES:
1. YOU ARE NOT A DOCTOR. Never diagnose the user. Never prescribe medication.
2. If the user expresses thoughts of self-harm or suicide, you MUST immediately provide emergency hotlines (e.g., dial 988 in the US) and urge them to seek professional help.
3. Base your therapeutic suggestions ONLY on the provided context below.

CONTEXT:
{context}

CONVERSATION HISTORY:
{history}

Respond to the user naturally and concisely:
"""
```
*Tuning Note:* Always keep the suicide/self-harm safety catch at the top of the prompt rules, as LLMs pay more attention to the beginning and end of instructions.

## 4. Chunking Strategy for Therapy Docs

In `3-embedding.py`, the way documents are split affects how the bot understands them.

- **`chunk_size`:** `800`.
- **`chunk_overlap`:** `150`.
*Reasoning:* Psychological concepts often take multiple sentences to explain (e.g., explaining the concept of "Cognitive Distortions"). If the chunk size is too small (e.g., 200), the bot might retrieve the definition but lose the practical examples provided in the subsequent sentences of the source text.
