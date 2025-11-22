import re
from pymongo import MongoClient
from langchain_core.documents import Document
from config import MONGO_URI

def clean_html(raw_html):
    if not isinstance(raw_html, str):
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def format_product_for_embedding(product):
    # Create a text representation for embedding
    text_parts = [
        f"Product Name: {product.get('name', 'N/A')}",
        f"Category: {product.get('category', 'N/A')}",
        f"Price: {product.get('price', 'N/A')}",
        f"Description: {product.get('description', 'N/A')}",
    ]
    
    # Add attributes if available
    if 'attributes' in product and isinstance(product['attributes'], dict):
        attrs = ", ".join([f"{k}: {v}" for k, v in product['attributes'].items()])
        text_parts.append(f"Attributes: {attrs}")
        
    return "\n".join(text_parts)

def load_products():
    client = MongoClient(MONGO_URI)
    db = client["test"] # Ensure using the correct DB name
    collection = db["products"]

    # Include _id to avoid issues, but we'll convert it to string in metadata
    raw_documents = list(
        collection.find({}, {"__v": 0, "images": 0, "createdAt": 0, "updatedAt": 0})
    )
    
    langchain_docs = []
    for doc in raw_documents:
        # Clean HTML in description
        if 'description' in doc:
            doc['description'] = clean_html(doc['description'])
            
        # Format content
        page_content = format_product_for_embedding(doc)
        
        # Prepare metadata
        metadata = {
            "name": doc.get('name', 'Unknown'),
            "category": doc.get('category', 'Unknown'),
            "price": str(doc.get('price', '0')),
            "id": str(doc.get('_id', ''))
        }
        
        # Create LangChain Document
        langchain_docs.append(Document(page_content=page_content, metadata=metadata))
        
    client.close()
    return langchain_docs

if __name__ == "__main__":
    docs = load_products()
    print(f"Loaded {len(docs)} documents.")
    if docs:
        print(docs[0])