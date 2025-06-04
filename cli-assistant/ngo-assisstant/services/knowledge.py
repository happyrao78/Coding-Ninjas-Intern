import os
import warnings
from typing import List
from rich.console import Console
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import with fallbacks
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings

        warnings.filterwarnings(
            "ignore", message=".*HuggingFaceEmbeddings.*deprecated.*"
        )
    except ImportError:
        HuggingFaceEmbeddings = None

try:
    from langchain_pinecone import PineconeVectorStore
    from pinecone import Pinecone
except ImportError:
    PineconeVectorStore = None
    Pinecone = None

console = Console()


class KnowledgeService:

    def __init__(self, config):
        self.config = config
        self.embeddings = None
        self.vector_store = None
        self._initialize_embeddings()
        self._initialize_pinecone()

    def _initialize_embeddings(self):
        """Initialize HuggingFace embeddings."""
        if HuggingFaceEmbeddings is None:
            console.print("[yellow]⚠️  HuggingFace embeddings not available[/yellow]")
            return

        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        except Exception as e:
            console.print(f"[yellow]⚠️  Embeddings initialization failed: {e}[/yellow]")

    def _initialize_pinecone(self):
        """Initialize Pinecone vector database."""
        api_key = self.config.get("pinecone_api_key")

        if not api_key or not self.embeddings or not Pinecone:
            console.print("[yellow]⚠️  Vector database disabled[/yellow]")
            return

        try:
            pc = Pinecone(api_key=api_key)
            index = pc.Index("ngo-knowledge-base")

            self.vector_store = PineconeVectorStore(
                index=index, embedding=self.embeddings
            )
            console.print("[green]✅ Connected to vector database[/green]")

        except Exception as e:
            console.print(f"[red]❌ Vector database connection failed: {e}[/red]")

    def load_from_file(self, file_path: str) -> bool:
        """Load knowledge from file."""
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, length_function=len
            )

            chunks = text_splitter.split_text(content)
            documents = [Document(page_content=chunk) for chunk in chunks]

            if self.vector_store:
                self.vector_store.add_documents(documents)
                console.print(
                    f"[green]✅ Loaded {len(documents)} knowledge chunks[/green]"
                )

            return True

        except Exception as e:
            console.print(f"[red]❌ Error loading knowledge: {e}[/red]")
            return False

    def search(self, query: str, k: int = 3) -> List[str]:
        """Search knowledge base for relevant information."""
        if not self.vector_store:
            return []

        try:
            docs = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            console.print(f"[red]Knowledge search error: {e}[/red]")
            return []
