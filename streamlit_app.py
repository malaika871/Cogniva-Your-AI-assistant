import streamlit as st
from src.config import Config
from src.document_processor import DocumentProcessor
from src.chatbot import Chatbot
from src.utils import check_ollama, ensure_model_available

# Modern UI Styling
st.set_page_config(
    page_title="Cogniva - Document Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #1e293b 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide default Streamlit UI elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Title styling */
    h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* Card styling */
    .modern-card {
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        background: rgba(15, 23, 42, 0.7);
        border-color: rgba(59, 130, 246, 0.3);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
    }
    
    /* Chat message styling */
    .user-message {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
        border-left: 3px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .assistant-message {
        background: rgba(30, 41, 59, 0.6);
        border-left: 3px solid #8b5cf6;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(139, 92, 246, 0.2);
        color: #e2e8f0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        letter-spacing: 0.3px;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(59, 130, 246, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* File uploader styling */
    .stFileUploader {
        border-radius: 10px;
        overflow: hidden;
    }
    
    .stFileUploader > div > div {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px dashed rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Spinner styling */
    .stSpinner {
        color: #3b82f6;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border-radius: 10px !important;
        border-left: 3px solid #22c55e !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border-radius: 10px !important;
        border-left: 3px solid #ef4444 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border-radius: 10px !important;
        border-left: 3px solid #f59e0b !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border-radius: 10px !important;
        border-left: 3px solid #3b82f6 !important;
    }
    
    /* Chat message containers */
    .stChatMessage {
        background: transparent !important;
        border-radius: 12px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-top: none;
        border-radius: 0 0 10px 10px;
    }
    
    /* Divider styling */
    hr {
        border: none;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin: 1.5rem 0;
    }
    
    /* Text styling */
    p, span, label, div {
        color: #e2e8f0;
    }
    
    h2, h3, h4, h5, h6 {
        color: #f1f5f9;
        font-weight: 600;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #60a5fa;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
        letter-spacing: 0.3px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 10px;
    }
    
    /* Metrics styling */
    .stMetric {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Display header
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("### ✨ Cogniva")
    with col2:
        st.markdown('<div class="subtitle">Your Intelligent Document Assistant</div>', unsafe_allow_html=True)
    
    # Check Ollama and model
    if not check_ollama():
        st.error("❌ Ollama is not running. Please ensure Ollama service is available.")
        st.info("For local setup: Run `ollama serve` in another terminal")
        st.stop()
    
    if not ensure_model_available(Config.OLLAMA_MODEL):
        st.stop()
    
    # Initialize session state
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = Chatbot()
        st.session_state.doc_processor = DocumentProcessor()
        st.session_state.messages = []
        st.session_state.document_loaded = False
    
    # Modern Sidebar
    with st.sidebar:
        st.markdown("### 📁 Document Management")
        st.markdown("---")
        
        # Upload section
        st.markdown("**Upload & Process**")
        uploaded_file = st.file_uploader(
            "Choose PDF or TXT file",
            type=['pdf', 'txt'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.caption(f"📄 {uploaded_file.name}")
            with col2:
                if st.button("✓", help="Load Document", key="load_doc_btn"):
                    with st.spinner("📖 Processing document..."):
                        text, pages = st.session_state.doc_processor.load_document(uploaded_file)
                        if text and "Error" not in text:
                            st.session_state.chatbot.load_document(
                                st.session_state.doc_processor.document_text,
                                uploaded_file.name
                            )
                            st.session_state.document_loaded = True
                            st.success(f"✅ Successfully loaded: {uploaded_file.name}")
                            st.info(f"📊 **Stats**: {len(text):,} chars • {pages} pages")
                            
                            with st.expander("Preview"):
                                st.text(text[:500])
                        else:
                            st.error("Failed to process document")
        
        st.markdown("---")
        
        # Document info section
        if st.session_state.document_loaded:
            st.markdown("### 📄 Active Document")
            st.markdown(f'<div class="badge">✓ {st.session_state.chatbot.get_document_name()}</div>', unsafe_allow_html=True)
            
            if st.button("🗑️ Clear Document", use_container_width=True):
                st.session_state.chatbot.clear_document()
                st.session_state.doc_processor.clear_document()
                st.session_state.document_loaded = False
                st.session_state.messages = []
                st.rerun()
        else:
            st.markdown("### 📄 Document Status")
            st.info("No document loaded. Upload a file to get started!")
        
        st.markdown("---")
        
        # Model info
        st.markdown("### ⚙️ Configuration")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="badge">Model: {Config.OLLAMA_MODEL}</div>', unsafe_allow_html=True)
        
        # Clear chat button
        st.markdown("---")
        if st.button("🔄 Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat area
    st.markdown("---")
    
    # Chat container
    st.markdown("### 💬 Chat")
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message"><strong>You:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            source_text = ""
            if "source" in msg:
                source = msg["source"]
                if "Document" in source:
                    source_text = ' <span class="badge">📄 Document</span>'
                else:
                    source_text = ' <span class="badge">🧠 AI</span>'
            st.markdown(f'<div class="assistant-message"><strong>Cogniva:</strong> {msg["content"]}{source_text}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Chat input
    prompt = st.chat_input(
        "Ask about your document..." if st.session_state.document_loaded else "Ask anything...",
        key="user_input"
    )
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    
    # Generate response if needed
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("✨ Thinking..."):
            last_user_msg = [m["content"] for m in st.session_state.messages if m["role"] == "user"][-1]
            use_document = st.session_state.document_loaded
            response, source, elapsed = st.session_state.chatbot.chat(last_user_msg, use_document)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "source": f"From: {'Document' if source == 'document' else 'AI'}"
            })
        
        st.rerun()

if __name__ == "__main__":
    main()
