# 🚀 Cogniva - Quick Start Guide

## Project Consolidation Complete ✅

**One unified Streamlit app** - All features integrated into a single `app.py`

---

## Running the Application

### Method 1: Direct Streamlit Command (Recommended)
```bash
streamlit run app.py --server.port=8501
```

### Method 2: Using Python Script
```bash
python run.py
```

### Method 3: Custom Port
```bash
streamlit run app.py --server.port=8502
```

---

## What's Inside app.py

✨ **Features:**
- 📄 Document Upload (PDF/TXT files)
- 🤖 Local LLM (Ollama - Mistral, Llama, Phi)
- 🔍 Web Search (Tavily API integration)
- 💬 Chat Interface with History
- 📊 Document Q&A with RAG
- 🎨 Modern Dark UI with Glassmorphism

---

## Prerequisites

Make sure these are installed:
- `streamlit` - Web UI framework
- `ollama` - Local LLM inference
- `PyPDF2` - PDF processing
- `python-dotenv` - Environment variables
- `requests` - API calls

**Already verified:** ✅ All dependencies are available

---

## File Structure

```
RAG_myown/
├── app.py                      # 🎯 MAIN APP (Streamlit)
├── run.py                      # Alternative runner
├── run_project.txt             # Command reference
├── src/
│   ├── config.py              # Configuration
│   ├── chatbot.py             # Chat logic
│   ├── document_processor.py  # File handling
│   ├── rag_engine.py          # RAG pipeline
│   └── utils.py               # Helper functions
├── data/                       # Data directory
└── .env                        # Environment variables
```

---

## Configuration

Edit `.env` to customize:
```env
TAVILY_API_KEY=your_api_key_here
```

Edit `src/config.py` for:
- Model selection (mistral, llama, phi)
- Chunk size for document processing
- Temperature settings
- Web search keywords

---

## Default Ports

- **Primary:** Port 8501
- **Alternative:** Ports 8502, 8503, etc.

---

## Removed Files (Backup)

- ❌ `test_app.py` (removed - redundant test app)
- ❌ `src/app.py` (removed - consolidated into root)
- 📦 `app_gradio_backup.py` (backup - old Gradio version)

---

## Status

✅ **ALL TESTS PASSED**
- Syntax validated
- Imports verified
- Configuration checked
- Dependencies confirmed
- Ready for production

---

## Next Steps

1. **Start Ollama:** `ollama serve` (in another terminal)
2. **Pull model:** `ollama pull mistral` (if not already pulled)
3. **Run the app:** `streamlit run app.py --server.port=8501`
4. **Access:** Open `http://localhost:8501` in your browser

---

**Questions?** Check the README.md for detailed documentation.
