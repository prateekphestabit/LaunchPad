import os
import pickle 
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib
import uuid
from typing import List
from dotenv import load_dotenv
from pathlib import Path

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(Path(CURR_DIR).parent / ".env")
    
def stable_id(text): #imagepath(for images) and  ocr + caption text() for text documents
    hash_bytes = hashlib.sha256(text.encode("utf-8")).digest()[:16]
    return str(uuid.UUID(bytes=hash_bytes))

class QdrantStore:
    def __init__(self, collection_name: str = "rag_multimodal", url: str = QDRANT_URL, vector_size: int = 512):
        self.collection_name = collection_name
        self.url = url
        self.vector_size = vector_size  # CLIP uses 512-dim
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        self.client = QdrantClient(url=self.url)
        
        # Check if collection exists
        collections = self.client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "image": VectorParams(
                        size=self.vector_size,  # CLIP embedding dimension
                        distance=Distance.COSINE
                    ),
                    "text": VectorParams(
                        size=self.vector_size,  # CLIP embedding dimension
                        distance=Distance.COSINE
                    )
                },
            )

    
    def add_text_documents(self, ocrCaptionTexts , embeddings):
        points = []
        for i, (ocrCaptionText, embedding) in enumerate(zip(ocrCaptionTexts, embeddings)):
            point_id = stable_id(ocrCaptionText['ocr_caption_text'])
            
            text_content = ocrCaptionText['ocr_caption_text']
            
            payload = dict(ocrCaptionText['metadata'])
            payload['content_type'] = 'text'
            payload['content'] = text_content
            payload['content_length'] = len(text_content)
            payload['doc_index'] = i
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector={"text": embedding.tolist(),},
                    payload=payload
                )
            )
        
        self._upsert_batch(points)
        print(f"Added {len(ocrCaptionTexts)} text documents to multimodal store")
    
    def add_images(self, ocrCaptionTexts, embeddings):
        points = []
        
        for i, (ocrCaptionText, embedding) in enumerate(zip(ocrCaptionTexts, embeddings)):
            # Generate stable ID from image path
            point_id = stable_id(ocrCaptionText['metadata']['path'])

            img_path = ocrCaptionText['metadata']['path']
            
            payload = dict(ocrCaptionText['metadata'])
            payload['content_type'] = 'image'
            payload['content'] = img_path
            payload['doc_index'] = i
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector={"image": embedding.tolist(),},
                    payload=payload
                )
            )
        
        self._upsert_batch(points)
        print(f"Added {len(ocrCaptionTexts)} images to multimodal store")
    
    def _upsert_batch(self, points: List[PointStruct], batch_size: int = 50):
        """Upsert points in batches"""
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                wait=True,
                points=batch
            )
        
        collection_info = self.client.get_collection(self.collection_name)
        print(f"Total documents in collection: {collection_info.points_count}")


# Create multimodal store instance
qdrant_multimodal_store = QdrantStore(
    collection_name="rag_multimodal",
    url=os.environ.get("qdranturl"),
    vector_size=512  # CLIP dimension
)


# Run ingestion only when this file is executed directly
if __name__ == "__main__":
    
    OCR_CAPTION_EMBEDDINGS_PATH = f'{CURR_DIR}/../data/cachedEmbeddings/ocr_caption_embeddings.npy'
    OCR_CAPTION_DOC_PATH  = f'{CURR_DIR}/../data/ocr_caption_text/ocr_caption_results.pkl'
    IMAGE_EMBEDDINGS_PATH = f'{CURR_DIR}/../data/cachedEmbeddings/image_embeddings.npy' 
    # Load embeddings
    ocr_embeddings = np.load(OCR_CAPTION_EMBEDDINGS_PATH)
    img_embeddings = np.load(IMAGE_EMBEDDINGS_PATH)
    # Load chunked documents
    with open(OCR_CAPTION_DOC_PATH, "rb") as f:
        ocr_caption_documents = pickle.load(f)
    
    # Add documents to vector store
    qdrant_multimodal_store.add_text_documents(ocr_caption_documents, ocr_embeddings)
    qdrant_multimodal_store.add_images(ocr_caption_documents, img_embeddings)