from pathlib import Path
from typing import List, Dict
from ..utils.pdf_utils import PDFProcessor
from .embedding_manager import EmbeddingManager
from .llm_manager import LLMManager

class QueryEngine:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.embedding_manager = EmbeddingManager()
        self.llm_manager = LLMManager()

    def add_document(self, pdf_path: Path):
        """Process and add a document to the system."""
        chunks = self.pdf_processor.process_pdf(pdf_path)
        self.embedding_manager.add_documents(chunks, pdf_path.name)

    def query(self, question: str, n_context: int = 5) -> str:
        """Query the system with a question."""
        # Get relevant context
        context_docs = self.embedding_manager.query_similar(question, n_context)
        
        # Generate response
        response = self.llm_manager.generate_response(question, context_docs)
        
        return response