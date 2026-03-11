# Multi-RAG System Interface

This Streamlit application integrates three RAG systems:

## Features

### 1. 📄 Ask (Text RAG) - Day 2
- **Flow**: User question → Hybrid Retriever → Groq LLM → Answer
- Uses hybrid search (dense embeddings + BM25)
- Generates contextual answers using Groq LLM
- Sources are cited in the response

### 2. 🖼️ Ask Image - Day 3
- **Flow**: User question → CLIP Embeddings → Image Search → Display Images
- Text-to-image search using CLIP embeddings
- Displays retrieved images with metadata
- Shows source PDF and page numbers

### 3. 🗄️ Ask SQL - Day 4
- **Flow**: User question → SQL Generator → Validator → Executor → Results + Summary
- Natural language to SQL conversion
- Automatic query validation and correction
- Displays results and AI-generated summary

## Setup

1. **Activate virtual environment**:
   ```bash
   source /home/prateek/Prateek/LaunchPad/week7/.venv/bin/activate
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure services are running**:
   ```bash
   # Start Qdrant (for Day2 and Day3)
   cd ../Day2
   docker compose up -d
   
   # Start PostgreSQL (for Day4)
   cd ../Day4
   docker compose up -d
   ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run deployment/app.py
   ```

## Usage

1. Open the app in your browser (usually http://localhost:8501)
2. Select a mode from the sidebar:
   - **Ask**: For document Q&A
   - **Ask Image**: For image search
   - **Ask SQL**: For database queries
3. Enter your question and click the action button
4. View results in the main panel

## Environment Variables

Make sure the following `.env` files exist:
- `Day2/.env` - Groq API credentials
- `Day4/.env` - PostgreSQL and Groq credentials