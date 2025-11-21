import re
from pymongo import MongoClient
from config import MONGO_URI

def clean_html(raw_html):
    if not isinstance(raw_html, str):
        return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()
        
def load_products():
    client = MongoClient(MONGO_URI)
    db = client["test"]
    collection = db["products"]

    raw_documents = list(
        collection.find({}, {"__v": 0, "images": 0, "createdAt": 0, "updatedAt": 0})
    )
    products = []
    for doc in raw_documents:
        # Clean HTML in description
        if 'description' in doc:
            doc['description'] = clean_html(doc['description'])
        
        products.append(doc)
        
    client.close()
    return products

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

if __name__ == "__main__":
    product = load_products()
    for doc in product:
        print(doc.keys())