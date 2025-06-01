import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    # Google Sheets
    google_sheets_credentials_file: str = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "credentials/google_sheets_creds.json")
    google_sheet_id: str = os.getenv("GOOGLE_SHEET_ID", "1QZM-5VXhXCpFM6LKlNbtzo7kiX-p4WX9uPfXJt9xAkQ")
    worksheet_name: str = os.getenv("WORKSHEET_NAME", "Sheet1")
    
    # Gemini
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # Custom Message
    custom_message: str = os.getenv("CUSTOM_MESSAGE", """
Greetings {ngo_name},

I'm Happy Yadav, a developer focused on building smart, scalable solutions. I create custom systems including ERP & CRM platforms, e-commerce solutions, and AI-powered automation tools tailored to your specific needs.

I'd be interested in discussing how my expertise might benefit your organization. Would you be available for a brief conversation this week?

Looking forward to your response.

Best regards,
Happy Yadav
www.happyrao.tech
""")
    
    # WhatsApp
    message_template: str = custom_message
    chrome_user_data_dir: str = os.getenv("CHROME_USER_DATA_DIR", "data/chrome_user_data")
    
    # Application
    processing_interval: int = int(os.getenv("PROCESSING_INTERVAL", "300"))  # Seconds between fetch/send cycles
    
    class Config:
        env_file = ".env"

settings = Settings()