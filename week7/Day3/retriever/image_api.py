import os
import torch
from typing import List, Dict
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from qdrant_client import QdrantClient

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
QDRANT_URL = "http://localhost:6344"
COLLECTION_NAME = "rag_multimodal"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed_text_query(text_query: str):
    with torch.no_grad():
        inputs = processor(
            text=text_query,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        )
        inputs = {k: v.to("cpu") for k, v in inputs.items()}
        outputs = model.get_text_features(**inputs)
        text_features = outputs / outputs.norm(p=2, dim=-1, keepdim=True)
        
    return text_features.cpu().numpy().flatten().tolist()


def search_images_by_text(text_query: str, top_k: int = 5) -> List[Dict]:
    """
    Search for images based on text query
    
    Args:
        text_query: User's text query
        top_k: Number of results to return
        
    Returns:
        List of dicts with image_path, source_pdf, score
    """
    # Embed the text query
    query_embedding = embed_text_query(text_query)
    
    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL)
    
    # Search in image vector space
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        using="image",
        limit=top_k,
        with_payload=True,
        score_threshold=0.0
    )
    
    # Format results
    formatted_results = []
    for result in results.points:
        payload = result.payload
        formatted_results.append({
            "image_path": payload.get('path', 'N/A'),
            "source_pdf": payload.get('source_pdf', 'N/A'),
            "page_number": payload.get('page_number', 'N/A'),
            "content_type": payload.get('content_type', 'N/A'),
            "score": result.score
        })
    
    return formatted_results


def ask_image(question: str, top_k: int = 5) -> List[Dict]:
    """
    Main API function to get images based on text query
    
    Args:
        question: User's question
        top_k: Number of images to return
        
    Returns:
        List of image results with paths and metadata
    """
    return search_images_by_text(question, top_k)
