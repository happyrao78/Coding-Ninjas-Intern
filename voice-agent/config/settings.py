from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    # Twilio Configuration
    twilio_account_sid: str = Field(..., description="Twilio Account SID")
    twilio_auth_token: str = Field(..., description="Twilio Auth Token")
    twilio_phone_number: str = Field(..., description="Twilio Phone Number")
    to_number: str = Field(..., description="Recipient Phone Number")
    webhook_url: str = Field(..., description="Webhook URL")
    
    # AI Service Configuration
    gemini_api_key: str = Field(..., description="Google Gemini API Key")
    langchain_api_key: Optional[str] = Field(None, description="LangChain API Key")
    langsmith_api_key: Optional[str] = Field(None, description="LangSmith API Key")
    langsmith_project: str = Field("voice-agent", description="LangSmith Project Name")
    
    # Email Configuration
    gmail_address: str = Field(..., description="Gmail Address")
    gmail_app_password: str = Field(..., description="Gmail App Password")
    
    # Database Configuration
    database_url: str = Field("sqlite:///data/voice_agent.db", description="Database URL")
    
    # Google Sheets Configuration
    google_credentials_path: str = Field("credentials/lofty-seer-457323-p7-99057e124a49.json", description="Google Credentials Path")
    google_sheet_name: str = Field("User data", description="Google Sheet Name")
    
    # Application Configuration
    app_name: str = Field("Voice Agent", description="Application Name")
    app_version: str = Field("1.0.0", description="Application Version")
    debug: bool = Field(False, description="Debug Mode")
    port: int = Field(8000, description="Server Port")
    
    # Agent Configuration
    default_language: str = Field("hi-IN", description="Default Language")
    voice_model: str = Field("Polly.Aditi", description="Voice Model")
    conversation_timeout: int = Field(10, description="Conversation Timeout in seconds")
    max_retries: int = Field(2, description="Maximum Retries")
    
    # Knowledge Base Configuration
    knowledge_base_path: str = Field("data/knowledge.txt", description="Knowledge Base File Path")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

# LangSmith Configuration
if settings.langsmith_api_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project