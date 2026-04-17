import streamlit as st
import ollama
import tempfile
import os

st.set_page_config(page_title="Test App", page_icon="✅", layout="wide")

st.title("🧠 Test App")
st.write("If you can see this, Streamlit is working!")

# Check Ollama
try:
    ollama.list()
    st.success("✅ Ollama is connected!")
except:
    st.error("❌ Ollama is not running. Run: `ollama serve`")

# Simple file upload
uploaded = st.file_uploader("Upload a text file", type=['txt'])

if uploaded:
    text = uploaded.read().decode('utf-8')
    st.text_area("File content:", text[:500])
    
    if st.button("Ask about this file"):
        prompt = f"Summarize this text: {text[:2000]}"
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        st.write(response['message']['content'])

st.info("If you see this, the app is running correctly!")