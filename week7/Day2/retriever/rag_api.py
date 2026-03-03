"""
API wrapper for Day2 RAG system to be used with Streamlit
"""
import sys
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
DAY2_DIR = os.path.dirname(CURR_DIR)

# Add Day2 to path for imports
sys.path.insert(0, DAY2_DIR)

from typing import Dict, Any, List
from VectorStore.qdrant import qdrant_store
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Document as QdrantDocument
from qdrant_client import models
from generator.generator import generate_answer

embedding_model = SentenceTransformer(f'{DAY2_DIR}/models/bge-base-en-v1.5')


class RAGRetriever:
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Run hybrid search with RRF fusion
        results = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection_name,
            prefetch=[
                models.Prefetch(
                    query=query_embedding.tolist(),
                    using="dense",
                    limit=top_k * 2
                ),
                models.Prefetch(
                    query=QdrantDocument(text=query, model="Qdrant/bm25"),
                    using="bm25",
                    limit=top_k * 2
                )
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=top_k,
            score_threshold=score_threshold
        )
        
        # Process results
        retrieved_docs = []
        for i, scored_point in enumerate(results.points):       
            retrieved_docs.append({
                'id': scored_point.id,
                'content': scored_point.payload.get('content', ''),
                'metadata': {k: v for k, v in scored_point.payload.items() if k != 'content'},
                'similarity_score': scored_point.score, 
                'rrf_score': scored_point.score,
                'rank': i + 1
            })
        
        return retrieved_docs


def ask_rag(question: str) -> str:
    """
    Main API function to get answer from RAG system
    
    Args:
        question: User's question
        
    Returns:
        Generated answer as string
    """
    # Initialize retriever
    rag_retriever = RAGRetriever(qdrant_store, embedding_model)
    
    # Retrieve documents
    retrieved_docs = rag_retriever.retrieve(question, top_k=5, score_threshold=0.0)
    
    # Generate answer using Groq
    answer = generate_answer(question, retrieved_docs)
    
    return answer
