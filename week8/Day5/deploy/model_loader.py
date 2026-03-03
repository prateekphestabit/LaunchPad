from llama_cpp import Llama
from config import GGUF_MODEL_PATH, N_CTX, N_THREADS
import os

# Global model instance — loaded once, reused for all requests
_model = None

def get_model() -> Llama:
    global _model
    if _model is None:
        print("Loading model...")
        _model = Llama(
            model_path=GGUF_MODEL_PATH,
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            verbose=False,
        )
        print("Model loaded and cached!")
    return _model