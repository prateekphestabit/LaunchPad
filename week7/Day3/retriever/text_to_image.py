import os
import sys
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from qdrant_client import QdrantClient

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
QDRANT_URL = "http://localhost:6333"
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
        
       
        text_features = outputs.pooler_output

        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
        
    return text_features.cpu().numpy().flatten().tolist()


def search_images_by_text(text_query, top_k = 5):
    from qdrant_client.models import NamedVector
    
    # Embed the text query
    query_embedding = embed_text_query(text_query)
    
    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL)
    
    # Search in image vector space using query_points
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        using="image",  # Search in image vectors
        limit=top_k,
        with_payload=True,
        score_threshold=0.0
    )
    
    return results.points


def display_results(results):
    """Display search results"""
    print("\n" + "="*60)
    print("TEXT TO IMAGE SEARCH RESULTS")
    print("="*60)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} (Score: {result.score:.4f}) ---")
        payload = result.payload
        print(f"  Image Path: {payload.get('path', 'N/A')}")
        print(f"  Source PDF: {payload.get('source_pdf', 'N/A')}")
        print(f"  Page Number: {payload.get('page_number', 'N/A')}")
        print(f"  Content Type: {payload.get('content_type', 'N/A')}")


if __name__ == "__main__":
    results = search_images_by_text("bispecific mutated", top_k=5)
    display_results(results)
