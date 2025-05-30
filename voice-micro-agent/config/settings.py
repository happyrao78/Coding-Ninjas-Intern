import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    TO_NUMBER = os.getenv("TO_NUMBER")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Email Configuration
    GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
    
    # Data Storage
    KNOWLEDGE_BASE_FILE = "data/knowledge.txt"
    USER_DATA_CSV = "data/user_data.csv"
    GOOGLE_CREDENTIALS_FILE = "credentials/lofty-seer-457323-p7-57f9ddecfb8b.json"

settings = Settings()