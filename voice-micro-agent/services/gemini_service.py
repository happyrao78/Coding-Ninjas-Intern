import google.generativeai as genai
from config.settings import settings

def setup_gemini():
    """Initialize Gemini AI"""
    try:
        if not settings.GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY not found")
            return False
        genai.configure(api_key=settings.GEMINI_API_KEY)
        return True
    except Exception as e:
        print(f"Error setting up Gemini: {e}")
        return False

def load_knowledge_base():
    """Load knowledge base data"""
    try:
        with open(settings.KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return "Knowledge base not found."

async def get_gemini_response(question):
    """Get response from Gemini for general questions"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Answer the following question in Hindi language. Keep the answer concise (2-3 sentences maximum).
        If you don't know the answer, just say you don't have that information in Hindi.
        
        Question: {question}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "मुझे इस सवाल का जवाब नहीं मिला। कृपया बाद में पुनः प्रयास करें।"

async def get_knowledge_base_response(question):
    """Get Gemini response using knowledge base"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        knowledge_base = load_knowledge_base()
        prompt = f"""
        You are a helpful AI assistant for Prereet Foundation.
        Use ONLY the following information to answer the user's question.
        If the answer isn't found in the provided information, politely say you don't have that information.
        Always answer in Hindi language. Keep the answer concise (2-3 sentences maximum).
        
        KNOWLEDGE BASE INFORMATION:
        {knowledge_base}
        USER QUESTION: {question}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting knowledge base response: {e}")
        return "मुझे इस सवाल का जवाब नहीं मिला। कृपया बाद में पुनः प्रयास करें।"

# Initialize Gemini on import
setup_gemini()