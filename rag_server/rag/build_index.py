from rag.mongo_loader import load_products
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import CHROMA_DB_PATH, EMBEDDING_MODEL
import shutil
import os

def build_index():
    print("Starting LangChain index build process...")
    
    # 1. Load data from Mongo
    print("Loading products from MongoDB...")
    documents = load_products()
    print(f"Loaded {len(documents)} documents.")
    
    if not documents:
        print("No documents found. Exiting.")
        return

    # 2. Initialize Embedding Model
    print(f"Loading embedding model: {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # 3. Create/Update Vector Store
    # Optional: Clear existing DB to avoid duplicates if rebuilding from scratch
    # if os.path.exists(CHROMA_DB_PATH):
    #     shutil.rmtree(CHROMA_DB_PATH)

    print("Creating Chroma vector store...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
        collection_name="products_rag"
    )
    
    print(f"Index build complete. Documents added to {CHROMA_DB_PATH}")

if __name__ == "__main__":
    build_index()
