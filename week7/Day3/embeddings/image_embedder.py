import numpy as np
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Union
import os
from io import BytesIO
import base64
import pickle

def generate_image_embeddings(imgPaths, model, processor):
    embeddings = []
    batch_size = 16  # Smaller batch for images due to memory
    
    with torch.no_grad():
        for i in range(0, len(imgPaths), batch_size):
            batch_images = imgPaths[i:i + batch_size]
            
            # Load images if paths are provided
            pil_images = []
            for imgPath in batch_images:
                pil_images.append(Image.open(imgPath).convert("RGB"))
                
            inputs = processor(
                images=pil_images,
                return_tensors="pt",
                padding=True
            )

            inputs = {k: v.to('cpu') for k, v in inputs.items()}
            
            # Get image features
            outputs = model.get_image_features(**inputs)
            
            # Handle different return types (tensor vs object with attributes)
            if hasattr(outputs, 'image_embeds'):
                image_features = outputs.image_embeds
            elif hasattr(outputs, 'pooler_output'):
                image_features = outputs.pooler_output
            else:
                image_features = outputs  # Already a tensor
            
            # Normalize embeddings
            image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
            
            embeddings.append(image_features.cpu().numpy())
    
    result = np.vstack(embeddings)
    print(f"Generated image embeddings of shape: {result.shape}")
    return result


def image_to_base64(image: Union[str, Image.Image], max_size: tuple = (512, 512)) -> str:
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = image
    
    # Convert to RGB if necessary
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # Resize to thumbnail while maintaining aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def base64_to_image(base64_string: str) -> Image.Image:
    image_data = base64.b64decode(base64_string)
    return Image.open(BytesIO(image_data))


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_META_DATA_DIR = os.path.join(CURR_DIR, "../data/imageMetaData")

with open(f'{IMAGE_META_DATA_DIR}/image_meta_data.pkl', "rb") as f:
    image_meta_data = pickle.load(f)

EMBEDDINGS_PATH = f'{CURR_DIR}/../data/cachedEmbeddings/image_embeddings.npy'
if os.path.exists(EMBEDDINGS_PATH):
    print("Loading cached embeddings from disk...")
    embeddings = np.load(EMBEDDINGS_PATH)
else:
    print("Generating embeddings...")
    imgPaths = [img_info["path"] for img_info in image_meta_data]
    imageEmbeddings = generate_image_embeddings(imgPaths, model, processor)
    np.save(EMBEDDINGS_PATH, imageEmbeddings)




