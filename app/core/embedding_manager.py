import os
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from ..config import CHROMA_DB_DIR

class EmbeddingManager:
    def __init__(self):
        # Ensure the directory exists with proper permissions
        os.makedirs(CHROMA_DB_DIR, exist_ok=True)
        
        # Set proper permissions for the directory
        os.chmod(CHROMA_DB_DIR, 0o777)
        
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_DIR,
            settings=Settings(
                allow_reset=True,
                anonymized_telemetry=False
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Dict], source: str):
        """Add documents to the collection."""
        if not documents:
            return
            
        # Generate unique IDs for each chunk
        ids = [f"{source}_{i}" for i in range(len(documents))]
        
        # Extract text content and metadata
        texts = [doc['content'] for doc in documents]
        metadatas = [{'source': source} for _ in documents]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )