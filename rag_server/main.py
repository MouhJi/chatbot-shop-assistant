from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from rag.retriever import retrieve_context
from rag.prompt_builder import build_prompt
from rag.gemini_client import generate_answer

app = FastAPI(title="RAG Server")

class QueryRequest(BaseModel):
    question: str

class Source(BaseModel):
    name: str
    info: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.post("/rag/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        # 1. Retrieve context
        context_list = retrieve_context(request.question)
        
        # 2. Build prompt
        prompt = build_prompt(request.question, context_list)
        
        # 3. Generate answer
        answer = generate_answer(prompt)
        
        # 4. Format sources
        sources = [
            {
                "name": item['metadata'].get('name'),
                "category": item['metadata'].get('category'),
                "price": item['metadata'].get('price')
            } 
            for item in context_list
        ]
        
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
