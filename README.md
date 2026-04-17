# ✨ Cogniva - Intelligent RAG Chatbot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![Ollama](https://img.shields.io/badge/Ollama-0.1.6+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**An intelligent chatbot with Document Q&A, Real-Time Web Search, and RAG capabilities**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Cogniva** is a powerful, privacy-focused chatbot that combines:
-  Document Q&A - Upload PDF/TXT files and ask questions
-  Real-Time Web Search - Get current information from the internet
-  Local LLM Processing - All data stays on your machine
-  RAG Architecture - Intelligent retrieval-augmented generation

Unlike cloud-based chatbots (ChatGPT, Claude), Cogniva runs **100% locally** using open-source models, ensuring complete privacy and zero API costs.

---

## ✨ Features

| Feature               Description

| Document Upload       Upload PDF and TXT files for analysis
| Document Q&A          Ask questions about your uploaded documents
| Web Search            Real-time web search for current events/news 
| RAG Pipeline          Retrieval-Augmented Generation for accurate answers
| Multiple LLMs         Support for Mistral, Llama, Phi, TinyLlama 
| Source Attribution    Shows whether answer came from document, web, or AI
| Chat History          Maintains conversation context
| Typing Indicator      Visual feedback while generating responses
| Glassmorphism UI      Modern, ChatGPT-style interface
| Privacy First         No data leaves your machine


## Tech Stack

   Core Technologies

  Technology   Version    Purpose

| Python       3.10+    Main programming language  
| Streamlit    1.29+    Web UI framework  
| Ollama       0.1.6+   Local LLM inference engine  
| LangChain    0.1.0    RAG orchestration 
| ChromaDB     0.4.22   Vector database for embeddings
| Tavily API   Latest   Web search integration

**LLM Models Supported**

  Model       Size    Quality      Speed   RAM

| Mistral     4.1GB | ⭐⭐⭐⭐⭐ | Slow |   6GB+ 
| Llama 3.2   4.7GB | ⭐⭐⭐⭐⭐ | Slow |   6GB+ 
| Phi-3 Mini  2.3GB | ⭐⭐⭐⭐   | Fast |   3GB+ 
| TinyLlama   637MB | ⭐⭐       | VeryFast 1GB+ 

### Python Dependencies

txt
streamlit==1.29.0          # Web UI framework
ollama==0.1.6              # Local LLM client
langchain==0.1.0           # RAG orchestration
langchain-community==0.0.10 # Community integrations
chromadb==0.4.22           # Vector database
sentence-transformers==2.2.2 # Text embeddings
PyPDF2==3.17.4             # PDF text extraction
python-dotenv==1.0.0       # Environment variables
requests==2.31.0           # HTTP requests (Tavily API)
tavily-python==0.3.1       # Web search API




**ARCHITECTURE**


┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Streamlit / Gradio)                       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        QUERY ROUTER                             │
│          Determines if question needs:                          │
│          • Document Search (RAG)                                │
│          • Web Search (Tavily)                                  │
│          • Both / Neither                                       │
└─────────────────────────────────────────────────────────────────┘
                    │                       │
                    ▼                       ▼
        ┌───────────────────┐    ┌───────────────────┐
        │   DOCUMENT RAG    │    │    WEB SEARCH     │
        │                   │    │                   │
        │  • PDF/TXT Loader │    │  • Tavily API     │
        │  • Text Chunking  │    │  • Result Filter  │
        │  • Embeddings     │    │  • Source Citation│
        │  • Vector Search  │    │                   │
        └───────────────────┘    └───────────────────┘
                    │                       │
                    └───────────┬───────────┘
                                ▼
                    ┌───────────────────┐
                    │   CONTEXT MERGE   │
                    │  Combine sources  │
                    └───────────────────┘
                                │
                                ▼
                    ┌───────────────────┐
                    │   LOCAL LLM       │
                    │   (Ollama)        │
                    │  • Mistral        │
                    │  • Llama 3.2      │
                    │  • Phi-3 Mini     │
                    └───────────────────┘
                                │
                                ▼
                    ┌───────────────────┐
                    │   RESPONSE        │
                    │  • Answer         │
                    │  • Source Badge   │
                    └───────────────────┘
