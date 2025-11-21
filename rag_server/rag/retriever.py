from rag.embedding import embedding_service
from rag.chroma_db import chroma_service

def retrieve_context(query, n_results=3):
    # 1. Embed the query
    query_embedding = embedding_service.embed_query(query)
    
    # 2. Search ChromaDB
    results = chroma_service.query(query_embedding, n_results=n_results)
    
    # 3. Format results
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    
    context_list = []
    for doc, meta in zip(documents, metadatas):
        context_list.append({
            "content": doc,
            "metadata": meta
        })
        
    return context_list
