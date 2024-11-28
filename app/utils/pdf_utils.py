from pathlib import Path
from typing import List, Dict
import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..config import MAX_CHUNK_SIZE, CHUNK_OVERLAP

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=MAX_CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )

    def extract_text(self, pdf_path: Path) -> str:
        """Extract text from a PDF file."""
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
        return text

    def process_pdf(self, pdf_path: Path) -> List[Dict[str, str]]:
        """Process PDF and return chunks with metadata."""
        text = self.extract_text(pdf_path)
        chunks = self.text_splitter.create_documents([text])
        
        return [{
            'content': chunk.page_content,
            'metadata': {
                'source': pdf_path.name,
                'chunk_index': i
            }
        } for i, chunk in enumerate(chunks)]