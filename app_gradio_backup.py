import gradio as gr
import ollama
import tempfile
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = "mistral"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
WEB_KEYWORDS = ["current", "latest", "today", "now", "recent", "breaking", "updates", "news", "war"]

def search_web(query):
    if not TAVILY_API_KEY:
        return None
    try:
        url = "https://api.tavily.com/search"
        payload = {"api_key": TAVILY_API_KEY, "query": query, "max_results": 3, "include_answer": True}
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            data = r.json()
            results = []
            if data.get("answer"):
                results.append({"content": data["answer"], "url": "Summary"})
            for res in data.get("results", [])[:2]:
                results.append({"content": res.get("content", "")[:500], "url": res.get("url", "")})
            return results
    except:
        pass
    return None

def process_file(file):
    if file is None:
        return None
    try:
        text = ""
        if file.name.endswith(".txt"):
            with open(file.name, "r", encoding="utf-8") as f:
                text = f.read()
        elif file.name.endswith(".pdf"):
            import PyPDF2
            with open(file.name, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        return text
    except:
        return None

document_text = ""
document_name = ""

def chat(message, history):
    global document_text, document_name
    use_web = any(k in message.lower() for k in WEB_KEYWORDS) and TAVILY_API_KEY
    web_results = search_web(message) if use_web else None
    if document_text and web_results:
        prompt = f"Document:\n{document_text[:3000]}\n\nWeb Results:\n{web_results[0]["content"]}\n\nQuestion: {message}\nAnswer using BOTH sources. Cite sources."
    elif document_text:
        prompt = f"Document:\n{document_text[:4000]}\n\nQuestion: {message}\nAnswer based ONLY on the document. If not found, say so."
    elif web_results:
        prompt = f"Web Results:\n{web_results[0]["content"]}\n\nQuestion: {message}\nAnswer based on web results. Cite sources."
    else:
        prompt = f"Question: {message}\nAnswer concisely."
    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}], options={"temperature": 0.7, "num_predict": 500})
        answer = response["message"]["content"]
        if document_text and web_results:
            answer += "\n\n---\n📄 From document + 🌐 Web search"
        elif document_text:
            answer += "\n\n---\n📄 From your document"
        elif web_results:
            answer += "\n\n---\n🌐 From web search"
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

def upload_file(file):
    global document_text, document_name
    if file:
        text = process_file(file)
        if text:
            document_text = text
            document_name = file.name
            return f"✅ Loaded: {file.name}"
    return "❌ Failed to load file"

def clear_document():
    global document_text, document_name
    document_text = ""
    document_name = ""
    return "📄 Document cleared"

with gr.Blocks(theme=gr.themes.Soft(), title="Cogniva") as demo:
    gr.Markdown("# ✨ Cogniva\n### Intelligent Assistant | Document Q&A | Web Search")
    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="Cogniva", height=500, bubble_full_width=False, avatar_images=(None, "🤖"))
            msg = gr.Textbox(label="Ask anything...", placeholder="Type your message here...", lines=1, scale=4)
            with gr.Row():
                send_btn = gr.Button("➤ Send", variant="primary", scale=1)
                clear_chat_btn = gr.Button("🗑️ Clear Chat", scale=1)
        with gr.Column(scale=1):
            gr.Markdown("### 📁 Documents")
            file_upload = gr.File(label="Upload PDF or TXT", file_types=[".pdf", ".txt"])
            upload_status = gr.Textbox(label="Status", interactive=False)
            clear_doc_btn = gr.Button("🗑️ Clear Document")
            gr.Markdown("---\n### 🌐 Web Search")
            if TAVILY_API_KEY:
                gr.Markdown("✅ Web search enabled")
            else:
                gr.Markdown("⚠️ Add TAVILY_API_KEY to .env")
            gr.Markdown("---\n### 💡 Examples\n- What's in my document?\n- Latest news on AI\n- Summarize this for me")
    chat_history = gr.State([])
    def respond(message, history):
        history = history or []
        history.append([message, None])
        response = chat(message, history)
        history[-1][1] = response
        return history, ""
    send_btn.click(respond, [msg, chat_history], [chatbot, msg])
    msg.submit(respond, [msg, chat_history], [chatbot, msg])
    def clear_chat():
        return [], []
    clear_chat_btn.click(clear_chat, None, [chatbot, chat_history])
    file_upload.upload(upload_file, [file_upload], [upload_status])
    clear_doc_btn.click(clear_document, None, [upload_status])

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
