import ollama
import time
from config import Config
from rag_engine import RAGEngine

class Chatbot:
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.current_document = None
    
    def load_document(self, text, name):
        """Load a document into the RAG engine"""
        self.rag_engine.set_document(text)
        self.current_document = name
    
    def has_document(self):
        """Check if a document is loaded"""
        return bool(self.rag_engine.document_text)
    
    def get_document_name(self):
        return self.current_document
    
    def clear_document(self):
        """Clear loaded document"""
        self.rag_engine.set_document("")
        self.current_document = None
    
    def chat(self, question, use_document=True):
        """Generate response - uses document if available"""
        
        if use_document and self.has_document():
            # Answer from document
            answer, elapsed = self.rag_engine.answer_from_document(question)
            return answer, "document", elapsed
        else:
            # General chat (no document)
            start_time = time.time()
            
            prompt = f"""You are a helpful AI assistant. Answer naturally.

Question: {question}

Answer:"""
            
            try:
                response = ollama.chat(
                    model=Config.OLLAMA_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    options={
                        "temperature": Config.TEMPERATURE_CHAT,
                        "num_predict": 500
                    }
                )
                elapsed = time.time() - start_time
                return response['message']['content'], "general", elapsed
            except Exception as e:
                return f"Error: {e}", "error", 0