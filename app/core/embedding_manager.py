from pathlib import Path
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from ..config import CHROMA_DB_DIR, EMBEDDING_MODEL

class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        # Updated Chroma client configuration
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, documents: List[Dict[str, str]], source: str):
        """Add documents to the vector store."""
        embeddings = self.model.encode([doc['content'] for doc in documents])
        
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=[doc['content'] for doc in documents],
            metadatas=[doc['metadata'] for doc in documents],
            ids=[f"{source}-{doc['metadata']['chunk_index']}" for doc in documents]
        )

    def query_similar(self, query: str, n_results: int = 5) -> List[Dict]:
        """Query similar documents."""
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        return [
            {
                'content': doc,
                'metadata': metadata
            }
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0])
        ]