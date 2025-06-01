import os
import json
import smtplib
from typing import List, Dict
from email.mime.text import MIMEText
from pathlib import Path
from email.mime.multipart import MIMEMultipart

from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm, Prompt

console = Console()

class EmailService:
    """Handles email sending functionality."""
    
    def __init__(self, config):
        self.config = config
    
    def send_single(self, to_email: str, subject: str, body: str, from_name: str = None) -> bool:
        """Send single email."""
        smtp_server = self.config.get('smtp_server')
        smtp_port = self.config.get('smtp_port', 587)
        email = self.config.get('email')
        password = self.config.get('email_password')
        
        if not all([smtp_server, email, password]):
            console.print("[yellow]  Email not configured[/yellow]")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{from_name or 'NGO Assistant'} <{email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, to_email, msg.as_string())
            server.quit()
            
            return True
            
        except Exception as e:
            console.print(f"[red] Email failed: {e}[/red]")
            return False
    
    def send_bulk(self, recipients: List[str], subject: str, body: str) -> Dict[str, int]:
        """Send bulk emails with progress tracking."""
        results = {'successful': 0, 'failed': 0}
        
        console.print(f"[cyan]📤 Sending to {len(recipients)} recipients...[/cyan]")
        
        for i, recipient in enumerate(recipients, 1):
            success = self.send_single(recipient, subject, body)
            
            if success:
                results['successful'] += 1
                console.print(f"[green] {i}/{len(recipients)}: {recipient}[/green]")
            else:
                results['failed'] += 1
                console.print(f"[red] {i}/{len(recipients)}: {recipient}[/red]")
            
            # Rate limiting
            import time
            time.sleep(0.5)
        
        return results
    
    def load_email_lists(self) -> Dict[str, List[str]]:
        """Load email lists from data directory."""
        email_lists = {}
        data_dir = Path('data')
        email_files = ['donors.txt', 'volunteers.txt', 'board_members.txt', 'media.txt']
        
        for file_name in email_files:
            file_path = data_dir / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        emails = [line.strip() for line in f if line.strip() and '@' in line]
                        list_name = file_name.replace('.txt', '')
                        email_lists[list_name] = emails
                except Exception as e:
                    console.print(f"[red] Error loading {file_name}: {e}[/red]")
        
        return email_lists
    
    def load_templates(self) -> Dict[str, str]:
        """Load email templates."""
        template_path = Path('data/email_templates.json')
        if not template_path.exists():
            return {}
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[red] Error loading templates: {e}[/red]")
            return {}