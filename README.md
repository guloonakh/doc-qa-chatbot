# DocChat — AI Document Q\&A Chatbot

> Upload any PDF and have a conversation with it. Powered by RAG (Retrieval-Augmented Generation), FAISS, LangChain, and LLaMA 3 via Groq.

!\[Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square\&logo=python)
!\[LangChain](https://img.shields.io/badge/LangChain-1.x-green?style=flat-square)
!\[Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square\&logo=streamlit)
!\[FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-orange?style=flat-square)
!\[Groq](https://img.shields.io/badge/Groq-LLaMA%203-purple?style=flat-square)
!\[License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

\---

## What it does

DocChat lets you upload any PDF and instantly ask questions about it in natural language. It answers accurately using only information from your document, cites the exact page numbers, and remembers the last 4 exchanges for multi-turn conversation.

\---

## Demo

**Asking about RAG — step-by-step explanation retrieved from the document:**

!\[Demo 1 - RAG explanation](assets/demo1.png)

**Asking about AI applications — table data correctly retrieved and listed:**

!\[Demo 2 - AI applications](assets/demo2.png)

**Asking a comparison question — multi-concept reasoning with page citations:**

!\[Demo 3 - ML vs Deep Learning](assets/demo3.png)

\---

## How it works

```
PDF Upload  →  PyMuPDF (extract text)  →  Chunker (500 tokens, 50 overlap)
           →  sentence-transformers (embed)  →  FAISS (store index)

User Question  →  Embed question  →  FAISS similarity search (top 4 chunks)
              →  Build prompt (context + history + question)
              →  LLaMA 3 via Groq  →  Answer + page citations
```

The key insight: instead of sending the whole PDF to the LLM (expensive, slow, hits token limits), we only send the 4 most relevant chunks. This makes it fast, cheap, and accurate.

\---

## Tech stack

|Layer|Technology|
|-|-|
|Frontend|Streamlit|
|PDF parsing|PyMuPDF (fitz)|
|Text chunking|LangChain RecursiveCharacterTextSplitter|
|Embeddings|sentence-transformers `all-MiniLM-L6-v2` (local, free)|
|Vector store|FAISS (persisted to disk)|
|LLM|LLaMA 3.1 8B via Groq API|
|Orchestration|LangChain|

\---

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/guloonakh/doc-qa-chatbot.git
cd doc-qa-chatbot
```

**2. Create a virtual environment**

```bash
python -m venv venv
venv\\Scripts\\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Get a free Groq API key**

Sign up at [console.groq.com](https://console.groq.com) — no credit card required.

**5. Add your API key**

```bash
# Create a .env file
echo "GROQ\_API\_KEY=your\_key\_here" > .env
```

**6. Run the app**

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

\---

## Project structure

```
doc-qa-chatbot/
├── app.py                  # Streamlit UI
├── rag/
│   ├── \_\_init\_\_.py
│   ├── ingestion.py        # PDF loading, chunking, embedding, FAISS indexing
│   └── retrieval.py        # Query embedding, retrieval, LLM call
├── requirements.txt
├── .env                    # API key (not committed)
├── .gitignore
└── assets/
    ├── demo1.png
    ├── demo2.png
    └── demo3.png
```

\---

## Features

* Upload any PDF — research papers, books, reports, CVs
* Natural language Q\&A grounded in your document
* Page number citations on every answer
* Multi-turn conversation memory (last 4 exchanges)
* Fully local embeddings — no data sent to external servers for indexing
* FAISS index persisted to disk — no re-indexing on page refresh
* Clear conversation button to reset context

\---

## Requirements

```
streamlit
langchain
langchain-community
langchain-groq
langchain-text-splitters
pymupdf
faiss-cpu
sentence-transformers
python-dotenv
```

\---

## \## Author

## 

## \*\*Guloona Khan\*\* — AI \& Machine Learning Engineer | Computer Vision | LLMs | Full-Stack AI

## 

## \[GitHub](https://github.com/guloonakh) • \[LinkedIn](https://www.linkedin.com/in/guloona-khan-a07419365)---



