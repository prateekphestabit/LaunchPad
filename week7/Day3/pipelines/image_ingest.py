import os
import fitz
from PIL import Image
from io import BytesIO
import pickle
import pytesseract
import torch
from transformers import BlipForConditionalGeneration, BlipProcessor


def extract_images(pdf_path, output_dir):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    doc = fitz.open(pdf_path)
    
    extracted = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Convert to PIL Image
            pil_image = Image.open(BytesIO(image_bytes))
            
            # Skip small images (likely icons/logos)
            if pil_image.width < 50 or pil_image.height < 50:
                continue
            
            # Save image
            image_filename = f"{pdf_name}_page{page_num + 1}_img{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_dir, image_filename)
            
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            
            extracted.append({
                "path": image_path,
                "source_pdf": pdf_path,
                "page_number": page_num + 1,
                "image_index": img_index + 1,
                "format": image_ext
            })

    doc.close()
    print(f"Extracted {len(extracted)} images from {pdf_path}")
    return extracted #contains all the images extracted from the pdf with their metadata

def extract_images_from_pdfs(PDF_DATA_DIR, IMG_DATA_DIR):
    all_images = []
    pdf_files = [f for f in os.listdir(PDF_DATA_DIR) if f.lower().endswith(".pdf")]
    
    print(f"\nFound {len(pdf_files)} PDF files to process")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DATA_DIR, pdf_file)
        images = extract_images(pdf_path, IMG_DATA_DIR)
        all_images.extend(images)
    
    print(f"\nTotal images extracted: {len(all_images)}")
    print(all_images)
    return all_images

def process_images_text(image_meta_data, OCR_CAPTION_DIR, processor, model):
    ocr_caption_path = os.path.join(OCR_CAPTION_DIR, "ocr_caption_results.pkl")
    
    ocr_caption_cache = []

    if os.path.exists(ocr_caption_path):
        with open(ocr_caption_path, "rb") as f:
            ocr_caption_cache = pickle.load(f)
        print(f"cached OCR + caption results present")
        return ocr_caption_cache
    
    for i, img_info in enumerate(image_meta_data):
        image_path = img_info["path"]
        print(f"\nProcessing image {i + 1}/{len(image_meta_data)}: {os.path.basename(image_path)}")
           
        # ===================>>> extracting text using OCR (tesseract)
        pil_image = Image.open(image_path)
        
        image = pil_image
        if image.mode != "RGB":
            image = image.convert("RGB")

        ocr_text = pytesseract.image_to_string(image, lang="eng")

        ocr_text = ocr_text.strip()
        ocr_text = " ".join(ocr_text.split()) 
        
        # ====================>>>  generating Caption using blip

        image = pil_image
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        
        inputs = processor(image, return_tensors="pt").to('cpu')

        with torch.no_grad():
            output = model.generate(**inputs, max_length=50)

        caption = processor.decode(output[0], skip_special_tokens=True)
        
        # =========================>> fullText = OCR + Caption
        full_text = ocr_text + " " + caption 
        ocr_caption_cache.append({
            "ocr_caption_text": full_text,
            "metadata": img_info
        })
    
    # Save caches
    with open(ocr_caption_path, "wb") as f:
        pickle.dump(ocr_caption_cache, f)
    
    print(ocr_caption_cache)    
    return ocr_caption_cache


processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DATA_DIR = os.path.join(CURR_DIR, "../data/Raw/pdf_data")
IMG_DATA_DIR = os.path.join(CURR_DIR, "../data/Raw/image_data")
IMAGE_META_DATA_DIR = os.path.join(CURR_DIR, "../data/imageMetaData")

if not os.path.exists(f'{IMAGE_META_DATA_DIR}/image_meta_data.pkl'):
    os.makedirs(IMAGE_META_DATA_DIR, exist_ok=True)
    image_meta_data = extract_images_from_pdfs(PDF_DATA_DIR, IMG_DATA_DIR)
    with open(f'{IMAGE_META_DATA_DIR}/image_meta_data.pkl', "wb") as f:
        pickle.dump(image_meta_data, f)
else:
    with open(f'{IMAGE_META_DATA_DIR}/image_meta_data.pkl', "rb") as f:
        image_meta_data = pickle.load(f)
    print("Loaded cached image metadata from disk.")
OCR_CAPTION_DIR = os.path.join(CURR_DIR, "../data/ocr_caption_text")

process_images_text(image_meta_data, OCR_CAPTION_DIR, processor, model)