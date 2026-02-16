import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from qdrant_client import QdrantClient

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "rag_multimodal"

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed_image_query(image_path: str):
    pil_image = Image.open(image_path).convert("RGB")
    
    with torch.no_grad():
        inputs = processor(
            images=pil_image,
            return_tensors="pt",
            padding=True
        )
        inputs = {k: v.to("cpu") for k, v in inputs.items()}
        outputs = model.get_image_features(**inputs)
        
        # Handle different return types
        if hasattr(outputs, 'image_embeds'):
            image_features = outputs.image_embeds
        elif hasattr(outputs, 'pooler_output'):
            image_features = outputs.pooler_output
        else:
            image_features = outputs  # Already a tensor
        
        # Normalize embedding
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
        
    return image_features.cpu().numpy().flatten().tolist()


def search_similar_images(image_path: str, top_k: int = 5):
    from qdrant_client.models import NamedVector
    
    # Embed the image query
    query_embedding = embed_image_query(image_path)
    
    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL)
    
    # Search in image vector space using query_points
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        using="image",  # Search in image vectors
        limit=top_k,
        with_payload=True
    )
    
    return results.points


def display_results(results, query_image_path: str):
    print("\n" + "="*60)
    print("IMAGE TO IMAGE SEARCH RESULTS")
    print("="*60)
    print(f"Query Image: {query_image_path}")
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} (Score: {result.score:.4f}) ---")
        payload = result.payload
        result_path = payload.get('path', 'N/A')
        
        # Check if it's the same image (self-match)
        is_self = os.path.abspath(result_path) == os.path.abspath(query_image_path) if result_path != 'N/A' else False
        
        print(f"  Image Path: {result_path}" + (" [SELF]" if is_self else ""))
        print(f"  Source PDF: {payload.get('source_pdf', 'N/A')}")
        print(f"  Page Number: {payload.get('page_number', 'N/A')}")
        print(f"  Content Type: {payload.get('content_type', 'N/A')}")


if __name__ == "__main__":
    image_path = "/home/prateek/Prateek/LaunchPad/week7/Day3Again/data/Raw/image_data/exchangeCommession_page6_img1.jpeg"
    
    results = search_similar_images(image_path, top_k=5)
    display_results(results, image_path)
