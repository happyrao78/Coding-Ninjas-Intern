#!/usr/bin/env python3
import os
import sys
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from pathlib import Path
import warnings

# Core imports
import click
import colorama
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

# Environment variables
from dotenv import load_dotenv

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# LangChain imports with fallback
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        warnings.filterwarnings("ignore", message=".*HuggingFaceEmbeddings.*deprecated.*")
    except ImportError as e:
        print(f"LangChain embeddings import error: {e}")
        HuggingFaceEmbeddings = None

try:
    from langchain_pinecone import PineconeVectorStore
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.schema import Document
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError as e:
    print(f"LangChain import error: {e}")

from pinecone import Pinecone
    


# Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# Initialize colorama and rich console
colorama.init()
console = Console()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress pydantic warnings
warnings.filterwarnings("ignore", message=".*Field.*model_client_cls.*conflict.*protected namespace.*")
warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")

class NGOConfig:
    """Configuration management for NGO agent using environment variables"""
    
    def __init__(self):
        # Load all config from environment variables
        self.config = {
            'gemini_api_key': os.getenv('GEMINI_API_KEY'),
            'pinecone_api_key': os.getenv('PINECONE_API_KEY'),
            'pinecone_environment': os.getenv('PINECONE_ENVIRONMENT', 'us-west1-gcp-free'),
            'email': os.getenv('EMAIL_ADDRESS'),
            'email_password': os.getenv('EMAIL_PASSWORD'),
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
        }
        
        # Check for missing critical environment variables
        self.check_env_vars()
    
    def check_env_vars(self):
        """Check if critical environment variables are set"""
        missing_vars = []
        
        if not self.config['gemini_api_key']:
            missing_vars.append('GEMINI_API_KEY')
        if not self.config['pinecone_api_key']:
            missing_vars.append('PINECONE_API_KEY')
            
        if missing_vars:
            console.print(f"[red]❌ Missing environment variables: {', '.join(missing_vars)}[/red]")
            console.print("[yellow]💡 Create a .env file with the following variables:[/yellow]")
            console.print("GEMINI_API_KEY=your_gemini_api_key")
            console.print("PINECONE_API_KEY=your_pinecone_api_key")
            console.print("PINECONE_ENVIRONMENT=us-west1-gcp-free")
            console.print("EMAIL=your_email@gmail.com")
            console.print("EMAIL_PASSWORD=your_app_password")
            console.print("SMTP_SERVER=smtp.gmail.com")
            console.print("SMTP_PORT=587")
            console.print("\n[cyan]Optional: Add email settings for email functionality[/cyan]")
        else:
            console.print("[green]✅ All critical environment variables loaded[/green]")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

class KnowledgeBase:
    """Manages NGO knowledge base with vector embeddings"""
    
    def __init__(self, config: NGOConfig):
        self.config = config
        self.embeddings = None
        self.vector_store = None
        self.pc = None  # Pinecone client
        self.initialize_embeddings()
        self.initialize_pinecone()
    
    def initialize_embeddings(self):
        """Initialize HuggingFace embeddings"""
        if HuggingFaceEmbeddings is None:
            console.print("[yellow]⚠️  HuggingFace embeddings not available[/yellow]")
            return
        
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        except Exception as e:
            console.print(f"[yellow]⚠️  Embeddings initialization failed: {e}[/yellow]")
    
    def initialize_pinecone(self):
        """Initialize Pinecone vector database"""
        api_key = self.config.get('pinecone_api_key')

        if not api_key:
            console.print("[yellow]⚠️  Pinecone API key not found - knowledge base disabled[/yellow]")
            return

        if not self.embeddings:
            console.print("[yellow]⚠️  Embeddings not available - knowledge base disabled[/yellow]")
            return

        try:
            # Initialize Pinecone client with new API
            pc = Pinecone(api_key=api_key)

            index_name = "ngo-knowledge-base"

            # List existing indexes
            index = pc.Index(index_name)

            # Connect to existing index (don't create new one)
            self.vector_store = PineconeVectorStore(
            index=index,
            embedding=self.embeddings
            )
            console.print("[green]✅ Connected to existing Pinecone index[/green]")
            

        except Exception as e:
            console.print(f"[red]❌ Pinecone initialization failed: {e}[/red]")
            console.print("[yellow]💡 Make sure your PINECONE_API_KEY is correct in .env file[/yellow]")
            
                
        
    def load_knowledge_from_file(self, file_path: str):
        """Load knowledge from knowledge.txt file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            
            chunks = text_splitter.split_text(content)
            documents = [Document(page_content=chunk) for chunk in chunks]
            
            if self.vector_store:
                self.vector_store.add_documents(documents)
                console.print(f"[green]✅ Loaded {len(documents)} knowledge chunks[/green]")
            else:
                console.print("[yellow]⚠️  Vector store not available - knowledge not loaded[/yellow]")
                
        except FileNotFoundError:
            console.print(f"[yellow]⚠️  Knowledge file {file_path} not found[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ Error loading knowledge: {e}[/red]")
    
    def search_knowledge(self, query: str, k: int = 3) -> List[str]:
        """Search knowledge base for relevant information"""
        if not self.vector_store:
            return []
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"Knowledge search error: {e}")
            return []

class EmailManager:
    """Handles email sending functionality"""
    
    def __init__(self, config: NGOConfig):
        self.config = config
    
    def send_email(self, to_email: str, subject: str, body: str, from_name: str = None):
        """Send email using SMTP"""
        smtp_server = self.config.get('smtp_server')
        smtp_port = self.config.get('smtp_port', 587)
        email = self.config.get('email')
        password = self.config.get('email_password')
        
        if not all([smtp_server, email, password]):
            console.print("[yellow]⚠️  Email configuration incomplete - add EMAIL, EMAIL_PASSWORD, SMTP_SERVER to .env[/yellow]")
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
            text = msg.as_string()
            server.sendmail(email, to_email, text)
            server.quit()
            
            console.print(f"[green]✅ Email sent successfully to {to_email}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Email sending failed: {e}[/red]")
            return False

class NGOAgent:
    """Main NGO conversational agent using Gemini"""
    
    def __init__(self, config: NGOConfig):
        self.config = config
        self.knowledge_base = KnowledgeBase(config)
        self.email_manager = EmailManager(config)
        self.llm = self.initialize_llm()
        self.conversation_history = []
        
    def initialize_llm(self):
        """Initialize Gemini LLM"""
        api_key = self.config.get('gemini_api_key')
        if not api_key:
            console.print("[red]❌ Gemini API key not found - AI features disabled[/red]")
            return None
        
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.7
            )
            console.print("[green]✅ Gemini AI initialized[/green]")
            return llm
        except Exception as e:
            console.print(f"[red]❌ LLM initialization failed: {e}[/red]")
            return None
    
    def get_context_from_knowledge(self, query: str) -> str:
        """Get relevant context from knowledge base"""
        relevant_chunks = self.knowledge_base.search_knowledge(query)
        if relevant_chunks:
            context = "\n\nRelevant NGO Information:\n" + "\n".join(relevant_chunks)
            return context
        return ""
    
    def generate_response(self, user_input: str) -> str:
        """Generate response using LLM with knowledge base context"""
        if not self.llm:
            return "AI model not available. Please set GEMINI_API_KEY in your .env file."
        
        # Get relevant context from knowledge base
        context = self.get_context_from_knowledge(user_input)
        
        # Create system prompt
        system_prompt = f"""You are an AI assistant for an NGO. You help with:
1. Campaign planning and strategy
2. Donation drive organization
3. Email communication
4. Event planning
5. Volunteer management

Use the NGO's specific information when available. Be helpful, professional, and action-oriented.

{context}

Current query: {user_input}

Provide a helpful response based on the NGO's context and needs."""

        try:
            response = self.llm.invoke(system_prompt)
            return response.content
        except Exception as e:
            logger.error(f"LLM response error: {e}")
            return f"Sorry, I encountered an error: {e}"
    
    def load_email_lists(self) -> Dict[str, List[str]]:
        """Load email lists from files"""
        email_lists = {}
        email_files = ['donors.txt', 'volunteers.txt', 'board_members.txt', 'media.txt']
        
        for file_name in email_files:
            if os.path.exists(file_name):
                try:
                    with open(file_name, 'r', encoding='utf-8') as f:
                        emails = [line.strip() for line in f if line.strip() and '@' in line]
                        list_name = file_name.replace('.txt', '')
                        email_lists[list_name] = emails
                        console.print(f"[green]✅ Loaded {len(emails)} emails from {file_name}[/green]")
                except Exception as e:
                    console.print(f"[red]❌ Error loading {file_name}: {e}[/red]")
        
        return email_lists

    def handle_email_request(self, user_input: str):
        """Handle email sending requests with multiple input methods"""
        console.print("[cyan]📧 Email Request Detected[/cyan]")
        
        # Check if email is configured
        if not all([self.config.get('email'), self.config.get('email_password'), self.config.get('smtp_server')]):
            console.print("[red]❌ Email not configured. Add EMAIL, EMAIL_PASSWORD, SMTP_SERVER to .env file[/red]")
            return
        
        # Load available email lists
        email_lists = self.load_email_lists()
        
        # Email input method selection
        console.print("\n[cyan]Choose email input method:[/cyan]")
        console.print("1. Enter single email manually")
        console.print("2. Use email list from file")
        console.print("3. Enter multiple emails (comma-separated)")
        
        if email_lists:
            console.print("\n[green]Available email lists:[/green]")
            for i, (list_name, emails) in enumerate(email_lists.items(), 4):
                console.print(f"{i}. {list_name.title()} ({len(emails)} emails)")
        
        choice = Prompt.ask("Select option", choices=[str(i) for i in range(1, 4 + len(email_lists))])
        
        recipients = []
        
        if choice == "1":
            recipient = Prompt.ask("Enter recipient email")
            recipients = [recipient]
            
        elif choice == "2":
            file_path = Prompt.ask("Enter email file path (e.g., my_emails.txt)")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    recipients = [line.strip() for line in f if line.strip() and '@' in line]
                console.print(f"[green]✅ Loaded {len(recipients)} emails from {file_path}[/green]")
            except FileNotFoundError:
                console.print(f"[red]❌ File {file_path} not found[/red]")
                return
                
        elif choice == "3":
            emails_input = Prompt.ask("Enter emails (comma-separated)")
            recipients = [email.strip() for email in emails_input.split(',') if email.strip()]
            
        else:
            list_index = int(choice) - 4
            list_name = list(email_lists.keys())[list_index]
            recipients = email_lists[list_name]
            console.print(f"[green]Selected {list_name} list with {len(recipients)} emails[/green]")
        
        if not recipients:
            console.print("[red]❌ No valid recipients found[/red]")
            return
        
        # Get email subject and body
        subject = Prompt.ask("Enter email subject")
        
        # Check for email templates with proper encoding
        templates = self.load_email_templates()
        if templates:
            console.print("\n[cyan]Available email templates:[/cyan]")
            for i, template_name in enumerate(templates.keys(), 1):
                console.print(f"{i}. {template_name}")
            console.print(f"{len(templates) + 1}. Write custom email")
            
            template_choice = Prompt.ask("Choose template", 
                                       choices=[str(i) for i in range(1, len(templates) + 2)])
            
            if int(template_choice) <= len(templates):
                template_name = list(templates.keys())[int(template_choice) - 1]
                body = templates[template_name]
                console.print(f"[green]✅ Using template: {template_name}[/green]")
            else:
                body = self.get_custom_email_body()
        else:
            body = self.get_custom_email_body()
        
        # Show preview
        self.show_email_preview(recipients, subject, body)
        
        # Confirm sending
        if Confirm.ask(f"\n[green]Send email to {len(recipients)} recipients?[/green]"):
            self.send_bulk_emails(recipients, subject, body)

    def load_email_templates(self) -> Dict[str, str]:
        """Load email templates from templates.json with proper encoding handling"""
        templates = {}
        if os.path.exists('email_templates.json'):
            try:
                # Try different encodings
                encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
                
                for encoding in encodings:
                    try:
                        with open('email_templates.json', 'r', encoding=encoding) as f:
                            templates = json.load(f)
                        console.print(f"[green]✅ Loaded {len(templates)} email templates[/green]")
                        break
                    except UnicodeDecodeError:
                        continue
                
                if not templates:
                    console.print("[yellow]⚠️  Could not read email templates due to encoding issues[/yellow]")
                    
            except json.JSONDecodeError as e:
                console.print(f"[red]❌ Invalid JSON in email templates: {e}[/red]")
            except Exception as e:
                console.print(f"[red]❌ Error loading templates: {e}[/red]")
        
        return templates

    def get_custom_email_body(self) -> str:
        """Get custom email body from user"""
        console.print("\n[cyan]Enter email content (type 'END' on a new line to finish):[/cyan]")
        body_lines = []
        while True:
            try:
                line = input()
                if line.strip() == 'END':
                    break
                body_lines.append(line)
            except KeyboardInterrupt:
                console.print("\n[yellow]Email input cancelled[/yellow]")
                return ""
        return '\n'.join(body_lines)

    def show_email_preview(self, recipients: List[str], subject: str, body: str):
        """Show email preview"""
        console.print("\n[yellow]📋 Email Preview:[/yellow]")
        preview_table = Table(show_header=True, header_style="bold magenta")
        preview_table.add_column("Field", style="cyan")
        preview_table.add_column("Content", style="white")
        
        recipient_display = ", ".join(recipients[:3])
        if len(recipients) > 3:
            recipient_display += f" ... and {len(recipients) - 3} more"
        
        preview_table.add_row("Recipients", f"{len(recipients)} emails")
        preview_table.add_row("To (sample)", recipient_display)
        preview_table.add_row("Subject", subject)
        preview_table.add_row("Body", body[:150] + "..." if len(body) > 150 else body)
        
        console.print(preview_table)

    def send_bulk_emails(self, recipients: List[str], subject: str, body: str):
        """Send emails to multiple recipients"""
        successful = 0
        failed = 0
        
        console.print(f"\n[cyan]📤 Sending emails to {len(recipients)} recipients...[/cyan]")
        
        for i, recipient in enumerate(recipients, 1):
            try:
                success = self.email_manager.send_email(recipient, subject, body)
                if success:
                    successful += 1
                    console.print(f"[green]✅ {i}/{len(recipients)}: {recipient}[/green]")
                else:
                    failed += 1
                    console.print(f"[red]❌ {i}/{len(recipients)}: {recipient}[/red]")
                    
                import time
                time.sleep(0.5)
                
            except Exception as e:
                failed += 1
                console.print(f"[red]❌ {i}/{len(recipients)}: {recipient} - {e}[/red]")
        
        # Summary
        console.print(f"\n[bold cyan]📊 Email Sending Summary:[/bold cyan]")
        console.print(f"[green]✅ Successful: {successful}[/green]")
        console.print(f"[red]❌ Failed: {failed}[/red]")
        console.print(f"[blue]📧 Total: {len(recipients)}[/blue]")
        
        self.conversation_history.append({
            'type': 'bulk_email_sent',
            'timestamp': datetime.now().isoformat(),
            'recipients_count': len(recipients),
            'successful': successful,
            'failed': failed,
            'subject': subject
        })
    
    def chat_loop(self):
        """Main chat loop"""
        console.print(Panel.fit(
            "[bold green]🌟 Welcome to NGO Campaign Assistant![/bold green]\n"
            "I can help you with campaign planning, donation drives, and email management.\n"
            "Type 'help' for commands, 'quit' to exit.",
            title="NGO Assistant",
            border_style="green"
        ))
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    console.print("[green]👋 Goodbye! Have a great day![/green]")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                
                elif 'send mail' in user_input.lower() or 'email' in user_input.lower():
                    self.handle_email_request(user_input)
                
                elif user_input.lower() == 'history':
                    self.show_history()
                
                elif user_input.lower() == 'env':
                    self.show_env_status()
                
                else:
                    # Generate AI response
                    with console.status("[bold green]Thinking...", spinner="dots"):
                        response = self.generate_response(user_input)
                    
                    console.print(f"\n[bold blue]🤖 Assistant:[/bold blue] {response}")
                    
                    self.conversation_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'user': user_input,
                        'assistant': response
                    })
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'quit' to exit properly.[/yellow]")
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
    
    def show_help(self):
        """Show help information"""
        help_table = Table(title="Available Commands", show_header=True)
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")
        
        commands = [
            ("help", "Show this help message"),
            ("send mail", "Send email to recipients"),
            ("history", "Show conversation history"),
            ("env", "Show environment variables status"),
            ("quit/exit", "Exit the application"),
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        console.print(help_table)
    
    def show_env_status(self):
        """Show environment variables status"""
        env_table = Table(title="Environment Variables Status", show_header=True)
        env_table.add_column("Variable", style="cyan")
        env_table.add_column("Status", style="white")
        
        env_vars = [
            ("GEMINI_API_KEY", "✅ Set" if self.config.get('gemini_api_key') else "❌ Missing"),
            ("PINECONE_API_KEY", "✅ Set" if self.config.get('pinecone_api_key') else "❌ Missing"),
            ("EMAIL", "✅ Set" if self.config.get('email') else "❌ Missing"),
            ("EMAIL_PASSWORD", "✅ Set" if self.config.get('email_password') else "❌ Missing"),
            ("SMTP_SERVER", "✅ Set" if self.config.get('smtp_server') else "❌ Missing"),
        ]
        
        for var, status in env_vars:
            env_table.add_row(var, status)
        
        console.print(env_table)
    
    def show_history(self):
        """Show conversation history"""
        if not self.conversation_history:
            console.print("[yellow]No conversation history yet.[/yellow]")
            return
        
        for entry in self.conversation_history[-5:]:
            timestamp = entry.get('timestamp', '')
            if entry.get('type') == 'bulk_email_sent':
                console.print(f"[dim]{timestamp}[/dim] [green]📧 Bulk email sent to {entry['recipients_count']} recipients[/green]")
            else:
                console.print(f"[dim]{timestamp}[/dim]")
                console.print(f"[cyan]You:[/cyan] {entry.get('user', '')}")
                console.print(f"[blue]Assistant:[/blue] {entry.get('assistant', '')[:100]}...")
                console.print("-" * 50)

@click.command()
@click.option('--knowledge-file', '-k', default='knowledge.txt', help='Path to knowledge base file')
def start(knowledge_file):
    """Start the NGO assistant chat interface"""
    console.print("[cyan]🚀 Starting NGO Assistant...[/cyan]")
    
    config = NGOConfig()
    agent = NGOAgent(config)
    
    # Load knowledge base if file exists
    if os.path.exists(knowledge_file):
        console.print(f"[cyan]📚 Loading knowledge from {knowledge_file}...[/cyan]")
        agent.knowledge_base.load_knowledge_from_file(knowledge_file)
    else:
        console.print(f"[yellow]💡 Create {knowledge_file} to add NGO-specific knowledge[/yellow]")
    
    # Start chat loop
    agent.chat_loop()

if __name__ == "__main__":
    start()