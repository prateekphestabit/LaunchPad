import os
import pickle 
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib
import uuid
from langchain_core.documents import Document
from typing import List


CURR_DIR = os.path.dirname(os.path.abspath(__file__))

    
def stable_id(doc: Document) -> str:
    #Generate a stable UUID from document content using SHA256 hash
    raw = doc.page_content
    # Create a SHA256 hash and use the first 16 bytes to create a UUID
    hash_bytes = hashlib.sha256(raw.encode("utf-8")).digest()[:16]
    return str(uuid.UUID(bytes=hash_bytes))

class QdrantVectorStore:
    def __init__(self, collection_name, url, vector_size):
        self.collection_name = collection_name
        self.url = url
        self.vector_size = vector_size
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        # Initialize Qdrant client and collection
        self.client = QdrantClient(url=self.url)
        
        # Check if collection exists, if not create it
        collections = self.client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            print(f"Created new collection: {self.collection_name}")
        else:
            print(f"Using existing collection: {self.collection_name}")
        
        # Get collection info
        collection_info = self.client.get_collection(self.collection_name)
        print(f"Vector store initialized with collection: {self.collection_name}")
        print(f"Existing documents in collection: {collection_info.points_count}")
    
    def add_documents(self, documents: List[Document], embeddings: np.ndarray):
        # Add documents and their embeddings to the Qdrant vector store
        
        points = []
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            # Generate unique id for each document
            #hex converts it to string of 8 cahrs uuid formant : f3c9a1e4-6b9e-4e9f-9a92-9d0c4e1c8c7a
            
            # point_id = f"doc_{uuid.uuid4().hex[:8]}_{i}" 
            # this is not a safe option redudant data will get pushed with different id 
            # so we will use hash of content as id 
            # also poiny_id accepst only unsigned int or UUIDs as string 
            point_id = stable_id(doc)
            
            # Prepare payload (metadata)
            payload = dict(doc.metadata)
            payload['doc_index'] = i
            payload['content_length'] = len(doc.page_content)
            payload['content'] = doc.page_content  # Store the actual text content
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload=payload
                )
            )
        
        # Upsert points in batches for better performance
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                wait=True,
                points=batch
            )
        
        # Get updated count
        collection_info = self.client.get_collection(self.collection_name)
        print(f"Tried to added {len(documents)} documents to the vector store.")
        print(f"Total documents in collection: {collection_info.points_count}")


# Create a reusable qdrant_store instance for querying (does NOT add documents on import)
qdrant_store = QdrantVectorStore(
    collection_name="rag_documents",
    url="http://localhost:6333",
    vector_size=768
)


# Run ingestion only when this file is executed directly
if __name__ == "__main__":
    EMBEDDINGS_PATH = f'{CURR_DIR}/../data/cachedEmbeddings/embeddings.npy'
    CHUNKED_DATA_PATH = f'{CURR_DIR}/../data/Chunked/chunked_documents.pkl'
    
    # Load embeddings
    embeddings = np.load(EMBEDDINGS_PATH)
    
    # Load chunked documents
    with open(CHUNKED_DATA_PATH, "rb") as f:
        chunked_documents = pickle.load(f)
    
    # Add documents to vector store
    qdrant_store.add_documents(chunked_documents, embeddings)