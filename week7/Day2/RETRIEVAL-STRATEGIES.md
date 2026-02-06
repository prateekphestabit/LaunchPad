## Retrieval Strategies

This project implements a hybrid retrieval pipeline for RAG, combining **dense vector search** with **sparse BM25 search** and fusing results using **Reciprocal Rank Fusion (RRF)**. It includes data ingestion, chunking, embedding generation, vector store setup (Qdrant), and a hybrid retriever.

## High-Level Pipeline

1. **Load raw documents** (CSV, DOCX, PDF, TXT)
2. **Clean & serialize** loaded documents
3. **Chunk** documents with overlap for better recall
4. **Generate embeddings** (BGE base) and cache them
5. **Index** dense + sparse vectors in Qdrant
6. **Hybrid retrieval** using dense + BM25 with RRF fusion


### => Hybrid Retriever (Dense + BM25 + RRF)

**File:** `retriever/hybrid_retriever.py`

- Encodes the query using the same BGE model.
- Executes **two prefetch searches**:
	- Dense vector search (`using="dense"`)
	- Sparse BM25 search (`using="bm25"`)
- Combines results using **RRF fusion** via Qdrant `FusionQuery`.
- Produces ranked results with:
	- `similarity_score` (RRF score)
	- `rank`
	- `metadata` and `content`
- Saves output to `retriever/retrieved.json`.

## Retrieval Strategy Details

### Dense Retrieval
- Captures semantic similarity using transformer embeddings.
- Strong for paraphrases and concept-level matches.

### Sparse Retrieval (BM25)
- Captures lexical overlap and exact keyword matching.
- Strong for precise terms, names, and rare keywords.

### Fusion (RRF)
   - RRF combines ranked lists from dense + sparse retrieval.
   
   - Benefits:
	- Improves recall by combining complementary signals.
	- More robust across different query styles.