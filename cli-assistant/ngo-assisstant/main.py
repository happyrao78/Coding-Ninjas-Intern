"""Main entry point for NGO Campaign Assistant."""

import click
from rich.console import Console
from rich.panel import Panel

from .core.agent import NGOAgent
from .config.settings import NGOConfig

console = Console()

@click.command()
@click.option('--knowledge-file', '-k', default='data/knowledge.txt', 
              help='Path to knowledge base file')
@click.version_option(version="1.0.0", prog_name="NGO Campaign Assistant")
def cli(knowledge_file):
    """Start the NGO Campaign Assistant chat interface."""
    console.print("[cyan]🚀 Starting NGO Assistant...[/cyan]")
    
    config = NGOConfig()
    agent = NGOAgent(config)
    
    # Load knowledge base if file exists
    if agent.load_knowledge(knowledge_file):
        console.print(f"[cyan]📚 Knowledge loaded from {knowledge_file}[/cyan]")
    else:
        console.print(f"[yellow]💡 Create {knowledge_file} to add NGO-specific knowledge[/yellow]")
    
    # Start chat loop
    agent.start_chat()

if __name__ == "__main__":
    cli()