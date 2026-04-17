import requests
import streamlit as st
import os

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_available_models():
    """Get list of downloaded models"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json()
            return [m['name'] for m in models.get('models', [])]
    except:
        pass
    return []

def ensure_model_available(model_name):
    """Check and prompt to download model if missing"""
    available = get_available_models()
    if model_name in available:
        return True
    
    st.warning(f"⚠️ Model '{model_name}' not found")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📥 Download {model_name}"):
            with st.spinner(f"Downloading {model_name}..."):
                os.system(f"ollama pull {model_name}")
                st.rerun()
            return False
    
    with col2:
        if st.button("📥 Download phi3:mini (Faster)"):
            with st.spinner("Downloading phi3:mini..."):
                os.system(f"ollama pull phi3:mini")
                st.success("Downloaded! Please update config to use 'phi3:mini'")
                st.rerun()
            return False
    
    return False