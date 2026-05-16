import ollama
import time
from .config import Config

class RAGEngine:
    def __init__(self):
        self.document_text = ""
    
    def set_document(self, text):
        """Set the document to use for RAG"""
        self.document_text = text
    
    def retrieve_relevant_context(self, question, max_chars=3000):
        """Simple keyword-based retrieval (no embeddings for speed)"""
        if not self.document_text:
            return ""
        
        question_lower = question.lower()
        question_words = set(question_lower.split())
        
        # Split document into chunks
        chunks = self.document_text.split('\n\n')
        
        # Score each chunk by keyword matches
        scored_chunks = []
        for chunk in chunks:
            chunk_lower = chunk.lower()
            score = sum(1 for word in question_words if word in chunk_lower)
            if score > 0:
                scored_chunks.append((score, chunk[:1000]))
        
        # Sort by relevance
        scored_chunks.sort(reverse=True)
        
        # Return top chunks
        relevant = [chunk for score, chunk in scored_chunks[:3]]
        
        if relevant:
            return "\n\n---\n\n".join(relevant)
        return ""
    
    def answer_from_document(self, question):
        """Generate answer based on document"""
        if not self.document_text:
            return None, 0
        
        start_time = time.time()
        
        # Retrieve relevant context
        context = self.retrieve_relevant_context(question)
        
        # Build prompt
        prompt = f"""You are a document analysis assistant. Answer based ONLY on the document below.

DOCUMENT CONTENT:
{self.document_text[:Config.MAX_DOCUMENT_CHARS]}

USER QUESTION: {question}

INSTRUCTIONS:
1. ONLY use information from the document
2. If the answer isn't in the document, say "The document does not contain this information"
3. Do NOT make up information

ANSWER:"""
        
        try:
            response = ollama.chat(
                model=Config.OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": Config.TEMPERATURE_DOCUMENT,
                    "num_predict": 500
                }
            )
            
            elapsed = time.time() - start_time
            return response['message']['content'], elapsed
            
        except Exception as e:
            return f"Error: {e}", 0