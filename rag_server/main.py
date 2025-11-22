from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from config import CHROMA_DB_PATH, EMBEDDING_MODEL, GEMINI_API_KEY

# Initialize FastAPI
app = FastAPI(title="RAG Server (LangChain)")

# --- LangChain Setup ---

# 1. Embeddings
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# 2. Vector Store & Retriever
vectorstore = Chroma(
    persist_directory=CHROMA_DB_PATH,
    embedding_function=embeddings,
    collection_name="products_rag"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. LLM (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

# 4. Prompt Template
from rag.prompt_builder import get_prompt_template

# 4. Prompt Template
prompt = get_prompt_template()

# 5. Chain Construction
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# --- API Endpoints ---

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.post("/rag/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        # Invoke the chain
        response = rag_chain.invoke({"input": request.question})
        
        # Extract answer and sources
        answer = response["answer"]
        context_docs = response["context"]
        
        sources = [
            {
                "name": doc.metadata.get('name', 'Unknown'),
                "category": doc.metadata.get('category', 'Unknown'),
                "price": doc.metadata.get('price', '0')
            } 
            for doc in context_docs
        ]
        
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
