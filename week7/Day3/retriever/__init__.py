"""
Multimodal Retriever Module

Three retrieval strategies:
1. text_to_image: Text query -> CLIP text embedding -> Search image vectors
2. image_to_text: Image query -> CLIP image embedding -> Search text vectors  
3. image_to_image: Image query -> CLIP image embedding -> Search image vectors
"""

from .text_to_image import search_images_by_text, embed_text_query
from .image_to_text import search_text_by_image, embed_image_query
from .image_to_image import search_similar_images

__all__ = [
    'search_images_by_text',
    'search_text_by_image', 
    'search_similar_images',
    'embed_text_query',
    'embed_image_query'
]
