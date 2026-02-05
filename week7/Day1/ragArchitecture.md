## Pipelines => ingest.py
   
   # converting to document data structure
   loads RAW data from data folder and convert all different data files to one Document data structure using these libararies 
    -> DirectoryLoader -------|
    -> TextLoader             |  
    -> PyMuPDFLoader          | ====>>> data/clean/all_documents.pkl
    -> Docx2txtLoader         |
    -> CSVLoader--------------|

   save all the documents to data/clean/all_documents.pkl directory

   # chunking all the documents
   after accumalating all the data we divide them into chunks using 
   
   # ==> RecursiveCharacterTextSplitter ===> data/Chunked/chunked_documents.pkl
   chunk_size == 800 tokens and 1 token == 1 char

## Embeddings => embedder.py

   # Implemented BGE_Base_Embedder classs to load and generate embeddings 
   
   1. Load chunked data from  <data/Chunked/chunked_documents.pkl>
   2. Generate Embeddings 
   3. Save embeddings to <data/cachedEmbeddings/embeddings.npy> (saves 6 mins)
   4. embedding dimension ====> <D-768>


## Vector Store => qdrant.py

   1. QdrantVectorStore class 
.      |=> Initialize client with:
.      |   *=> <QdrantClient_url == http://localhost:6333>
.      |        # qdrant running in docker container
.      |        # with mounted volume on <data/vectorStore:/qdrant/storage>
.      |
.      |=> Initialize Collection with: 
.      |   |=> <collection_name == rag_documents>     
.      |   *=> <vector_config>
.      |        |=> <vector_size == 768>
.      |        *=> <distance_formula == COSINE>
.      |   
.       *=> Function_to_Add_Data_To_VectorStore_Collection: 
.          *=> <collection_contains_points_array> 
.            *=> <points_array_contents>
.              |=> <id == stable_id>
.              |   # generated using content hash 
.              |   #exactly same content get's discarded 
.              | 
.              |=> <payload>
.              |   |=> <doc_index> 
.              |   |=> <content_length>
.              |   *=> <content>
.              |
.               *=> <vector_embeddings>

   2. Load embeddigns from <data/cachedEmbeddings/embeddings.npy>
   3. Load chunked data from <data/Chunked/chunked_documents.pkl>
   4. <qdrant_store.add_documents( chunked_documents, embeddings)>

## retriever => query_engine.py

   1. AppendPathToSys:
        |=><path == #/home/prateek/Prateek/LaunchPad/week7/Day1> 
        |=> <sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))>
        *=> <from VectorStore.qdrant import qdrant_store> 
   
   2. RAGRetriever class
      |
      |=> Initlize with:
      |   |=> <vector_store ==imported qdrant_store >
      |   *=> <embedding_model == SentenceTransformer("./models/bge-base-en-v1.5")>
      | 
      *=> Retrieve function:
          |=> <Parameters == <query,top_k,score_threshold>>:
          |=> <query_embedding(2D_array) == <self.embedding_model.encode( [query])[0]>> 
          *=> RESULT = from query_points:
               |=> <collection_name == rag_documents>
               |=> <query == query_embedding.tolist()>
               |=> <limit == 5>
               *=> <score_threshold == 0.0>
   
   3. retrieve docs and save them in a retrieved.json </retriever/reterieved.json>