import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
