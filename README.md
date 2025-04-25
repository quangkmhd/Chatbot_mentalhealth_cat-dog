# 🐾 Pet Mental Health Assistant
A Streamlit-based AI assistant that helps pet owners assess their pets' mental health by analyzing uploaded PDF documents and user-provided symptoms. It uses LLMs, vector embeddings, and BLEU scoring to retrieve and evaluate relevant health advice.
## 📌 Table of Contents
- [Introduction](#-introduction)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dependencies](#-dependencies)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributors](#-contributors)
- [License](#-license)
## 🧠 Introduction
**Pet Mental Health Assistant** provides an interactive chatbot interface for pet owners to understand possible mental health issues their pets might be facing. Users can upload veterinary PDFs, input symptoms, and receive personalized advice powered by large language models and retrieval-augmented generation (RAG).
## ✨ Features
* 📄 Upload and process PDF documents with mental health guidelines.
* 🔍 Semantic search using FAISS vector store.
* 💬 Chatbot interface powered by HuggingFace LLM (Mixtral-8x7B).
* ✅ BLEU Score evaluation against reference responses.
* 🐶 Pet profile manager for personalized context.
* 🧾 Saves and loads chat history across sessions.
* 📋 Symptom checklist for quick input.
## ⚙️ Installation
1. **Clone the repository**
```bash
git clone https://github.com/your-username/pet-mental-health-assistant.git
cd pet-mental-health-assistant
```
2. **Create a virtual environment and activate it**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Set up environment variables**
Create a `.env` file in the root directory:
```ini
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```
## ▶️ Usage
Run the Streamlit app:
```bash
streamlit run app.py
```
Once the interface loads in your browser, you can:
* Upload a PDF document with pet mental health content.
* Enter symptoms or use the checklist.
* Get personalized analysis and suggested actions.
* View BLEU Score comparing chatbot output with reference answers.
## 📦 Dependencies
* `streamlit`
* `PyMuPDF` (fitz)
* `langchain`
* `HuggingFaceHub`
* `nltk`
* `faiss-cpu`
* `python-dotenv`
* `sentence-transformers`
* `streamlit_chat`
Install all via:
```bash
pip install -r requirements.txt
```
## ⚙️ Configuration
* `HUGGINGFACEHUB_API_TOKEN`: Required for accessing the LLM from HuggingFace.
* `data/`: Default directory for storing:
  * Uploaded PDFs
  * FAISS vector stores
  * Pickled chat history
## 🗂 Project Structure
```
.
├── app.py                              # Main Streamlit app
├── prompt_template.py                  # Template used for chatbot prompts
├── requirements.txt
├── .env                                # Environment variables
├── data/
│   ├── chat_history.pkl
│   └── pet_mental_health_vector_store.pkl
```
## 🧪 Examples
**Input Symptom**:
```
My dog is hiding a lot and not eating.
```
**Output**:
Based on your pet's symptoms, they might be experiencing depression (70%) or anxiety (60%). Try maintaining a stable routine and consult a vet if the behavior persists.
**BLEU Score**: 0.65
## 🛠 Troubleshooting
| Issue | Solution |
|-------|----------|
| `No module named 'fitz'` | Install PyMuPDF: `pip install pymupdf` |
| BLEU score always "N/A" | Ensure the input symptom matches reference keywords. |
| FAISS not loading | Try deleting the `.pkl` file and re-uploading the PDF. |
## 👥 Contributors
* Nguyễn Hữu Quang – Initial development and design
## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🖼️ Application Preview

![Pet Mental Health Assistant Interface](img/screenshot-1743931538134.png)
[Pet Mental Health Assistant Interface](img/screenshot-1743931729684.png)

*Screenshot showing the Pet Mental Health Assistant interface with symptom input, PDF upload, and chatbot response.*
