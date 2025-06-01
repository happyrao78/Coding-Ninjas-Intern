from app.config import settings

class GeminiClient: 
    def __init__(self):
        self.initialized = True
        self.custom_message = settings.custom_message
    
    def initialize(self):
        """Initialize client with custom message"""
        return True
     
    def generate_message(self, ngo_name, context=None):
        """Return the custom message with the NGO name inserted"""
        try:
            return self.custom_message.format(ngo_name=ngo_name)
        except Exception as e:
            print(f"Error formatting custom message: {e}")
            # Fallback to simple template
            return f"Greetings {ngo_name}, I'm Happy Yadav. Looking forward to connecting with you."