import chromadb
from config import CHROMA_DB_PATH

class ChromaService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection_name = "products_rag"
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        
    def add_documents(self, documents, metadatas, ids, embeddings):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        
    def query(self, query_embedding, n_results=5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
    def count(self):
        return self.collection.count()

# Singleton instance
chroma_service = ChromaService()
