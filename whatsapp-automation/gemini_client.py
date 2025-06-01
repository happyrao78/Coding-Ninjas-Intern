import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient: 
    def __init__(self):
        self.initialized = True
        self.custom_message = os.getenv("CUSTOM_MESSAGE", """
        Greetings {ngo_name},
        
        I'm Happy Yadav, a developer focused on building smart, scalable solutions. I create custom systems including ERP & CRM platforms, e-commerce solutions, and AI-powered automation tools tailored to your specific needs.
        
        I'd be interested in discussing how my expertise might benefit your organization. Would you be available for a brief conversation this week?
        
        Looking forward to your response.
        
        Best regards,
        Happy Yadav
        www.happyrao.tech
        """)
    
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