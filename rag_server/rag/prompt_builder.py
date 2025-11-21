def build_prompt(query, context_list):
    context_str = "\n\n".join([f"Source: {item['metadata'].get('name', 'Unknown')}\nInfo: {item['content']}" for item in context_list])
    
    prompt = f"""Bạn là trợ lý AI hữu ích cho một cửa hàng thương mại điện tử.
Hãy sử dụng ngữ cảnh sau để trả lời câu hỏi của người dùng.
Nếu câu trả lời không nằm trong ngữ cảnh, hãy nói bạn không biết, nhưng hãy cố gắng hỗ trợ dựa trên thông tin có sẵn.
Đừng bịa đặt thông tin.

Context:
{context_str}

User Question: {query}

Answer:"""
    return prompt
