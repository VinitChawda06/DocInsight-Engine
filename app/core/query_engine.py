from pathlib import Path
from typing import List, Dict
import streamlit as st
from ..utils.pdf_utils import PDFProcessor
from .embedding_manager import EmbeddingManager
from .llm_manager import LLMManager

class QueryEngine:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.embedding_manager = EmbeddingManager()
        self.llm_manager = LLMManager()
        
        # Cache for processed documents
        if 'processed_docs' not in st.session_state:
            st.session_state.processed_docs = set()

    def add_document(self, pdf_path: Path):
        """Process and add a document to the system."""
        # Check if document is already processed
        if pdf_path.name in st.session_state.processed_docs:
            return
            
        chunks = self.pdf_processor.process_pdf(pdf_path)
        self.embedding_manager.add_documents(chunks, pdf_path.name)
        st.session_state.processed_docs.add(pdf_path.name)

    def query(self, question: str, n_context: int = 3) -> str:
        """Query the system with a question."""
        # Get similar documents based on the question
        context_docs = self.embedding_manager.query_similar(question, n_context)
        
        # Cache the LLM response generation
        @st.cache_data(show_spinner=False)
        def get_cached_response(q: str, context_str: str) -> str:
            return self.llm_manager.generate_response(q, context_str)
        
        # Prepare the context string
        context_str = "\n".join(doc.get('content', '') for doc in context_docs)
        
        return get_cached_response(question, context_str)