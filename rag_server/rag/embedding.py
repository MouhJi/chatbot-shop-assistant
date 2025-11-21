from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class EmbeddingService:
    def __init__(self):
        print(f"Loading embedding model: {EMBEDDING_MODEL} on CPU...")
        self.model = SentenceTransformer(EMBEDDING_MODEL, device='cpu')
        
    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()
        
    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

# Singleton instance
embedding_service = EmbeddingService()
