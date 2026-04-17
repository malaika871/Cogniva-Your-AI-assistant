import tempfile
import os
import streamlit as st

class DocumentProcessor:
    def __init__(self):
        self.document_text = ""
        self.document_name = ""
    
    def extract_from_pdf(self, file_path):
        """Extract text from PDF"""
        text = ""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {i+1} ---\n"
                        text += page_text
            return text, len(reader.pages)
        except Exception as e:
            return f"Error: {e}", 0
    
    def extract_from_txt(self, file_path):
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text, len(text.split('\n'))
        except Exception as e:
            return f"Error: {e}", 0
    
    def load_document(self, uploaded_file):
        """Load and store document"""
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # Extract based on file type
        if uploaded_file.name.endswith('.pdf'):
            text, pages = self.extract_from_pdf(tmp_path)
        else:
            text, pages = self.extract_from_txt(tmp_path)
        
        # Store
        self.document_text = text
        self.document_name = uploaded_file.name
        
        # Clean up
        os.unlink(tmp_path)
        
        return text, pages
    
    def get_document_preview(self, length=500):
        """Get preview of document"""
        if not self.document_text:
            return None
        return self.document_text[:length]
    
    def clear_document(self):
        """Clear loaded document"""
        self.document_text = ""
        self.document_name = ""