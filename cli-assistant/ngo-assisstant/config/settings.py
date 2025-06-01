import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from rich.console import Console


load_dotenv()
console = Console()

class NGOConfig:
    
    def __init__(self):
        self.config = {
            'gemini_api_key': os.getenv('GEMINI_API_KEY'),
            'pinecone_api_key': os.getenv('PINECONE_API_KEY'),
            'pinecone_environment': os.getenv('PINECONE_ENVIRONMENT', 'us-west1-gcp-free'),
            'email': os.getenv('EMAIL_ADDRESS'),
            'email_password': os.getenv('EMAIL_PASSWORD'),
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
        }
        self._validate_config()
    
    def _validate_config(self):
        """Validate critical environment variables."""
        missing_vars = []
        
        if not self.config['gemini_api_key']:
            missing_vars.append('GEMINI_API_KEY')
        if not self.config['pinecone_api_key']:
            missing_vars.append('PINECONE_API_KEY')
            
        if missing_vars:
            console.print(f"[red] Missing environment variables: {', '.join(missing_vars)}[/red]")
            console.print("[yellow] Create a .env file with required variables[/yellow]")
        else:
            console.print("[green]✅ Configuration loaded successfully[/green]")
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.config.get(key, default)