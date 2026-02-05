from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import pickle

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

def dataLoader(fileType, dataDirectory, loaderClass):
    dir_loader = DirectoryLoader(
        f'{CURR_DIR}/../data/Raw/{dataDirectory}',
        glob=f'*.{fileType}', 
        # *.txt loads all txt files in data/text_files directory (top level)
        # **/*.txt loads all txt files in the directory and subdirectories
        loader_cls=loaderClass,
    )
    return dir_loader.load()

def split_documents(documents, chunk_tokens, overlap_tokens):
    #Split documents into smaller chunks for better RAG performance
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_tokens, #800 chars per chunk 
        chunk_overlap = overlap_tokens, #150 chars shared with next chunk
        length_function=len, #function to select unit of length in this case chars
        # length function accepts only a function so direct values will not work
        # length_function=len(texts.split()), #function to select unit of length in this case words
        separators=["\n\n", "\n", " ", ""] #if chunk is beg split on para -> line -> space -> chars
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")
    
    return chunks



##Loading Documents
csvDocuments  = dataLoader('csv', 'csv_data', CSVLoader)
docxDocuments = dataLoader('docx', 'docx_data', Docx2txtLoader)
pdfDocuments  = dataLoader('pdf', 'pdf_data', PyMuPDFLoader)
textDocuments = dataLoader('txt', 'text_data', TextLoader)

all_documents = (
    csvDocuments +
    docxDocuments +
    pdfDocuments +
    textDocuments
)

print(f'Loaded a total of {len(all_documents)} documents.')
cleaned_data_path = os.path.join(CURR_DIR, "../data/Cleaned/cleaned_documents.pkl")

with open(cleaned_data_path, "wb") as f:
    pickle.dump(all_documents, f)

print("cleaned Documents saved successfully.")


##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> chunking documents <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#use all_documents from above or load from cleaned_documents.pkl
# with open(cleaned_data_path, "rb") as f:
#     all_documents = pickle.load(f)

chunked_documents = split_documents(all_documents, chunk_tokens=800, overlap_tokens=150)

chunked_data_path = os.path.join(CURR_DIR, "../data/Chunked/chunked_documents.pkl")

with open(chunked_data_path, "wb") as f:
    pickle.dump(chunked_documents, f)

print("chunked Documents saved successfully.")