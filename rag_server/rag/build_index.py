from rag.mongo_loader import load_products, format_product_for_embedding
from rag.embedding import embedding_service
from rag.chroma_db import chroma_service

def build_index():
    print("Starting index build process...")
    
    # 1. Load data from Mongo
    print("Loading products from MongoDB...")
    products = load_products()
    print(f"Loaded {len(products)} products.")
    
    if not products:
        print("No products found. Exiting.")
        return

    # 2. Prepare data for Chroma
    documents = []
    metadatas = []
    ids = []
    
    print("Processing products...")
    for product in products:
        # Create text for embedding
        text = format_product_for_embedding(product)
        documents.append(text)
        
        # Create metadata (store essential info for retrieval/display)
        meta = {
            "name": product.get('name', 'Unknown'),
            "category": product.get('category', 'Unknown'),
            "price": str(product.get('price', '0')),
            "id": str(product.get('_id', ''))
        }
        metadatas.append(meta)
        
        ids.append(str(product.get('_id')))
        
    # 3. Embed documents
    print("Embedding documents (this may take a while on CPU)...")
    embeddings = embedding_service.embed_documents(documents)
    
    # 4. Add to Chroma
    print("Adding to ChromaDB...")
    chroma_service.add_documents(documents, metadatas, ids, embeddings)
    
    print(f"Index build complete. Total documents in index: {chroma_service.count()}")

if __name__ == "__main__":
    build_index()
