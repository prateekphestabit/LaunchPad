from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import os
import pickle


### Embedder Class for BGE Base Model
class BGE_Base_Embedder:
    def __init__(self):
        self.model_name = "BAAI/bge-base-en-v1.5"  
        self.model = None
        self._load_model()

    def _load_model(self):
        print('loading model:', self.model_name)
        self.model = SentenceTransformer(self.model_name)
        self.model.save("./models/bge-base-en-v1.5")
        print('model loaded successfully Embedding Dimension:', self.model.get_sentence_embedding_dimension())
 
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts)
        print('generated embeddings of shape:', embeddings.shape)
        return embeddings


embedder = BGE_Base_Embedder()

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNKED_DATA_PATH = f'{CURR_DIR}/../data/Chunked/chunked_documents.pkl'

# Load chunked documents
with open(CHUNKED_DATA_PATH, "rb") as f:
    chunked_documents = pickle.load(f)

extracted_texts = [doc.page_content for doc in chunked_documents]

# Generated embedding 
# Embedding again and again was taking too much time so cached it on disk just for demo purpose
EMBEDDINGS_PATH = f'{CURR_DIR}/../data/cachedEmbeddings/embeddings.npy'
if os.path.exists(EMBEDDINGS_PATH):
    print("Loading cached embeddings from disk...")
# Add documents to vector store
    embeddings = np.load(EMBEDDINGS_PATH)
else:
    print("Generating embeddings...")
    embeddings = embedder.generate_embeddings(extracted_texts)
    np.save(EMBEDDINGS_PATH, embeddings)
