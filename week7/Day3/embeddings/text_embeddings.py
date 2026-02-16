from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np
import os
import pickle

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def generate_text_embeddings(texts):
    embeddings = []

    with torch.no_grad():
        for i in range(0, len(texts)):
            batch_texts = texts[i]["ocr_caption_text"]

            inputs = processor(
                text=batch_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=77
            )
            
            inputs = {k: v.to("cpu") for k, v in inputs.items()}
            tensor = model.get_text_features(**inputs)
            embedding = tensor.pooler_output
            embedding = embedding / embedding.norm(p=2, dim=-1, keepdim=True)
            embeddings.append(embedding.cpu().numpy())

    result = np.vstack(embeddings)
    print(f"Generated text embeddings of shape: {result.shape}")
    return result

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKED_DATA_PATH = os.path.join(CURR_DIR, "../data/Chunked/chunked_documents.pkl")


##===================> ocr + caption data embeddings
OCR_CAPTION_PATH = os.path.join(CURR_DIR, "../data/ocr_caption_text/ocr_caption_results.pkl")

with open(OCR_CAPTION_PATH, "rb") as f:
    ocr_caption_texts = pickle.load(f)

OCR_CAPTION_EMBEDDINGS_PATH = f'{CURR_DIR}/../data/cachedEmbeddings/ocr_caption_embeddings.npy'
if os.path.exists(OCR_CAPTION_EMBEDDINGS_PATH):
    print("Loading cached OCR + caption embeddings from disk...")
    ocr_caption_embeddings = np.load(OCR_CAPTION_EMBEDDINGS_PATH)
else:
    print("Generating OCR + caption embeddings...")
    # print(ocr_caption_texts[0]["ocr_caption_text"])
    ocr_caption_embeddings = generate_text_embeddings(ocr_caption_texts)
    np.save(OCR_CAPTION_EMBEDDINGS_PATH, ocr_caption_embeddings)