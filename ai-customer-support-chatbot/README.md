# 🤖 AI Customer Support Chatbot (Open-Source & Free)

A production-ready AI Assistant designed for web development and digital marketing agencies. This chatbot uses **Retrieval-Augmented Generation (RAG)** to answer customer queries based on company knowledge documents, running entirely on your local machine with **0% API costs**.

## 🌟 Project Overview
This project solves the problem of providing 24/7 customer support without the high costs of human agents or paid LLM APIs (like OpenAI). By using a local LLM (Ollama) and a vector database (FAISS), it remains private, secure, and fast.

## 🚀 How RAG Works (Simple Explanation)
1. **Knowledge Upload**: You upload your company PDFs or TXT files.
2. **Brain Chunking**: The system breaks these documents into small, manageable pieces.
3. **Library Indexing**: Each piece is converted into a mathematical "vector" and stored in a digital library (FAISS).
4. **Smart Retrieval**: When a customer asks a question, the assistant finds the most relevant pieces from the library.
5. **Contextual Answer**: It feeds those pieces + the question to the AI (Ollama) to generate a human-like, accurate response.

## 🏗️ Architecture
- **Frontend**: Streamlit (Beautiful, intuitive chat interface)
- **Backend API**: FastAPI (High-performance REST API)
- **AI Engine**: Ollama (Local Llama3 or Mistral)
- **Vectors**: FAISS (Fast local similarity search)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Orchestration**: LangChain

## 🛠️ Setup Instructions

### 1. Install Ollama
Download and install [Ollama](https://ollama.com/). Once installed, open your terminal and pull the Llama3 model:
```bash
ollama pull llama3
```

### 2. Python Environment
Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

## 🏃 How to Run Locally

### Step 1: Start the Backend (FastAPI)
In one terminal:
```bash
python -m backend.main
```
The API will be available at `http://localhost:8000`.

### Step 2: Start the Frontend (Streamlit)
In a second terminal:
```bash
streamlit run frontend/app.py
```
The UI will open in your browser at `http://localhost:8501`.

## 📸 Usage
1. Open the Streamlit UI.
2. Use the Sidebar to upload `company_knowledge.txt` (found in `data/`).
3. Click "Process Documents".
4. Start chatting! Ask about services, pricing, or hours.

## 🔮 Future Improvements
- **Multi-tenant support**: Handle multiple companies separately.
- **Voice Integration**: Allow customers to speak their queries.
- **WhatsApp/Slack Integration**: Connect to popular messaging platforms via Webhooks.
- **Automatic Web Scraping**: Periodically update knowledge from the company website.

---
Built with ❤️ for the Open Source Community.
