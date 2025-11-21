import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_answer(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error calling Gemini: {e}")
        return f"Xin lỗi, tôi đang gặp vấn đề: {str(e)}"
