# flow

## piplines => image_ingest.py
              |=> extract images from pdf to <data/Raw/image_data>
              |=> save image metadata to <data/imageMetaData>
              |=> extract OCR text from images using <tesseract>
              |=> generating caption from images using <blip>
              |=> final text data = OCR text + caption saved to <data/ocr_caption_text>


##                                     embeddings
                                      /          \
                          image_embedder.py      text_embeddings.py
                                                     \=> embeddings of [ocr + caption] text

## inserting embeddings into DB => qdrant.py

## retriever 
    => image to image
    => image to text
    => text to image

