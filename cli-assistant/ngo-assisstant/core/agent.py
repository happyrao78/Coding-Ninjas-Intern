from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from ..services.knowledge import KnowledgeService
from ..services.email import EmailService
from ..utils.helpers import EmailHandler

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

console = Console()


class NGOAgent:

    def __init__(self, config):
        self.config = config
        self.knowledge_service = KnowledgeService(config)
        self.email_service = EmailService(config)
        self.email_handler = EmailHandler(self.email_service)
        self.llm = self._initialize_llm()
        self.conversation_history = []

    def _initialize_llm(self):
        """Initialize Gemini LLM."""
        api_key = self.config.get("gemini_api_key")
        if not api_key or not ChatGoogleGenerativeAI:
            console.print("[red]❌ AI features disabled[/red]")
            return None

        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", google_api_key=api_key, temperature=0.7
            )
            console.print("[green]✅ AI initialized[/green]")
            return llm
        except Exception as e:
            console.print(f"[red]❌ AI initialization failed: {e}[/red]")
            return None

    def load_knowledge(self, file_path: str) -> bool:
        """Load knowledge base from file."""
        return self.knowledge_service.load_from_file(file_path)

    def generate_response(self, user_input: str) -> str:
        """Generate AI response with knowledge context."""
        if not self.llm:
            return (
                "AI model not available. Please set GEMINI_API_KEY in your .env file."
            )

        # Get relevant context
        context = self.knowledge_service.search(user_input)
        context_str = "\n".join(context) if context else ""

        system_prompt = f"""You are an AI assistant for an NGO. You help with:
1. Campaign planning and strategy
2. Donation drive organization  
3. Email communication
4. Event planning
5. Volunteer management

{f"Relevant context: {context_str}" if context_str else ""}

Query: {user_input}

Provide a helpful, professional response."""

        try:
            response = self.llm.invoke(system_prompt)
            return response.content
        except Exception as e:
            return f"Sorry, I encountered an error: {e}"

    def start_chat(self):
        """Main chat interface."""
        console.print(
            Panel.fit(
                "[bold green]🌟 Welcome to Sankalpiq's Campaign Assistant![/bold green]\n"
                "I can help with campaigns, donations, and email management.\n"
                "Type 'help' for commands, 'quit' to exit.",
                title="NGO Assistant",
                border_style="green",
            )
        )

        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()

                if user_input.lower() in ["quit", "exit", "bye"]:
                    console.print("[green]👋 Goodbye![/green]")
                    break

                elif user_input.lower() == "help":
                    self._show_help()

                elif any(word in user_input.lower() for word in ["send mail", "email"]):
                    self.email_handler.handle_email_request()

                elif user_input.lower() == "history":
                    self._show_history()

                elif user_input.lower() == "status":
                    self._show_status()

                else:
                    with console.status("[bold green]Thinking...", spinner="dots"):
                        response = self.generate_response(user_input)

                    console.print(f"\n[bold blue]🤖 Assistant:[/bold blue] {response}")

                    self.conversation_history.append(
                        {
                            "timestamp": datetime.now().isoformat(),
                            "user": user_input,
                            "assistant": response,
                        }
                    )

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'quit' to exit.[/yellow]")
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")

    def _show_help(self):
        """Show available commands."""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")

        commands = [
            ("help", "Show this help message"),
            ("send mail", "Send emails to recipients"),
            ("history", "Show conversation history"),
            ("status", "Show system status"),
            ("quit/exit", "Exit the CLI application"),
        ]

        for cmd, desc in commands:
            help_table.add_row(cmd, desc)

        console.print(help_table)

    def _show_history(self):
        """Show recent conversation history."""
        if not self.conversation_history:
            console.print("[yellow]No conversation history.[/yellow]")
            return

        for entry in self.conversation_history[-5:]:
            timestamp = entry.get("timestamp", "")
            console.print(f"[dim]{timestamp}[/dim]")
            console.print(f"[cyan]You:[/cyan] {entry.get('user', '')}")
            console.print(
                f"[blue]Assistant:[/blue] {entry.get('assistant', '')[:100]}..."
            )
            console.print("-" * 50)

    def _show_status(self):
        """Show system status."""
        status_table = Table(title="System Status")
        status_table.add_column("Component", style="cyan")
        status_table.add_column("Status", style="white")

        components = [
            ("AI (Gemini)", "✅ Ready" if self.llm else "❌ Disabled"),
            (
                "Knowledge Base",
                "✅ Ready" if self.knowledge_service.vector_store else "❌ Disabled",
            ),
            (
                "Email Service",
                "✅ Ready" if self.config.get("email") else "❌ Not configured",
            ),
        ]

        for component, status in components:
            status_table.add_row(component, status)

        console.print(status_table)
