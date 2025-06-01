"""Utility functions and helper classes."""

from pathlib import Path
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm, Prompt

console = Console()

class EmailHandler:
    """Handles email workflow and user interactions."""
    
    def __init__(self, email_service):
        self.email_service = email_service
    
    def handle_email_request(self):
        """Handle complete email sending workflow."""
        console.print("[cyan]📧 Email Campaign Manager[/cyan]")
        
        # Get recipients
        recipients = self._get_recipients()
        if not recipients:
            return
        
        # Get subject and body
        subject = Prompt.ask("Enter email subject")
        body = self._get_email_body()
        
        # Show preview and confirm
        self._show_preview(recipients, subject, body)
        
        if Confirm.ask(f"Send email to {len(recipients)} recipients?"):
            results = self.email_service.send_bulk(recipients, subject, body)
            self._show_results(results, len(recipients))
    
    def _get_recipients(self) -> List[str]:
        """Get email recipients through user interaction."""
        email_lists = self.email_service.load_email_lists()
        
        console.print("\n[cyan]Select recipient source:[/cyan]")
        options = [
            "Enter single email",
            "Enter multiple emails (comma-separated)",
            "Load from file"
        ]
        
        # Add email list options
        for list_name, emails in email_lists.items():
            options.append(f"Use {list_name} list ({len(emails)} emails)")
        
        for i, option in enumerate(options, 1):
            console.print(f"{i}. {option}")
        
        choice = int(Prompt.ask("Choose option", choices=[str(i) for i in range(1, len(options) + 1)]))
        
        if choice == 1:
            email = Prompt.ask("Enter email address")
            return [email] if email else []
        
        elif choice == 2:
            emails_input = Prompt.ask("Enter emails (comma-separated)")
            return [email.strip() for email in emails_input.split(',') if email.strip()]
        
        elif choice == 3:
            file_path = Prompt.ask("Enter file path")
            return self._load_emails_from_file(file_path)
        
        else:
            # Email list selection
            list_index = choice - 4
            list_name = list(email_lists.keys())[list_index]
            return email_lists[list_name]
    
    def _load_emails_from_file(self, file_path: str) -> List[str]:
        """Load emails from specified file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and '@' in line]
        except FileNotFoundError:
            console.print(f"[red]❌ File {file_path} not found[/red]")
            return []
    
    def _get_email_body(self) -> str:
        """Get email body from user or template."""
        templates = self.email_service.load_templates()
        
        if templates:
            console.print("\n[cyan]Available templates:[/cyan]")
            template_names = list(templates.keys())
            
            for i, name in enumerate(template_names, 1):
                console.print(f"{i}. {name}")
            console.print(f"{len(template_names) + 1}. Write custom email")
            
            choice = int(Prompt.ask("Choose template", 
                                  choices=[str(i) for i in range(1, len(template_names) + 2)]))
            
            if choice <= len(template_names):
                return templates[template_names[choice - 1]]
        
        # Custom email input
        console.print("\n[cyan]Enter email content (type 'END' on new line to finish):[/cyan]")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            except KeyboardInterrupt:
                console.print("\n[yellow]Email input cancelled[/yellow]")
                return ""
        
        return '\n'.join(lines)
    
    def _show_preview(self, recipients: List[str], subject: str, body: str):
        """Show email preview before sending."""
        console.print("\n[yellow]📋 Email Preview[/yellow]")
        
        preview_table = Table()
        preview_table.add_column("Field", style="cyan")
        preview_table.add_column("Content", style="white")
        
        sample_recipients = ", ".join(recipients[:3])
        if len(recipients) > 3:
            sample_recipients += f" ... (+{len(recipients) - 3} more)"
        
        preview_table.add_row("Recipients", f"{len(recipients)} total")
        preview_table.add_row("Sample", sample_recipients)
        preview_table.add_row("Subject", subject)
        preview_table.add_row("Body", body[:150] + ("..." if len(body) > 150 else ""))
        
        console.print(preview_table)
    
    def _show_results(self, results: Dict[str, int], total: int):
        """Show email sending results."""
        console.print(f"\n[bold cyan]📊 Email Campaign Results[/bold cyan]")
        
        results_table = Table()
        results_table.add_column("Status", style="cyan")
        results_table.add_column("Count", style="white")
        
        results_table.add_row("✅ Successful", str(results['successful']))
        results_table.add_row("❌ Failed", str(results['failed']))
        results_table.add_row("📧 Total", str(total))
        
        console.print(results_table)