import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#/home/prateek/Prateek/LaunchPad/week7/Day1

import json
from typing import Dict, Any, List
from VectorStore.qdrant import qdrant_store
from sentence_transformers import SentenceTransformer


# Add parent directory to path for imports
embedding_model = SentenceTransformer("./models/bge-base-en-v1.5")

class RAGRetriever:
    #Handles query-based retrieval from the vector store
    
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        print("Retrieving documents for query:", query)
        print("Top K:", top_k, "Score threshold:", score_threshold)
        
        # Generate query embedding
        # Embeddings are returned in a 2D array like [E1[1,2,3], E2[4,5,6]] therefore we use [0] to get first embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        results = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection_name,
            query=query_embedding.tolist(),
            limit=top_k,
            score_threshold=score_threshold
        )
        
        # Process results
        retrieved_docs = []
        print(f"Raw results count: {len(results.points)}")
        
        for i, scored_point in enumerate(results.points):
            retrieved_docs.append({
                'id': scored_point.id,
                'content': scored_point.payload.get('content', ''),
                'metadata': {k: v for k, v in scored_point.payload.items() if k != 'content'},
                'similarity_score': scored_point.score,  # Qdrant returns similarity score directly (for COSINE)
                'rank': i + 1
            })
        
        print(f"Retrieved {len(retrieved_docs)} documents")
        return retrieved_docs


# Use the imported qdrant_store (connects to existing collection)
rag_retriever = RAGRetriever(qdrant_store, embedding_model)

# Retrieve documents and save to JSON file
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(CURR_DIR, "retrieved.json")

retrieved_docs = rag_retriever.retrieve("sheryl baxter working at rasmussen group")

# Save to JSON file
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(retrieved_docs, f, indent=2, ensure_ascii=False)

print(f"Retrieved {len(retrieved_docs)} documents and saved to {OUTPUT_FILE}")