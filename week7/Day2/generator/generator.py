import os
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)

def generate_answer(question: str, retrieved_docs: List[Dict[str, Any]]) -> str:
    # Build context from retrieved documents
    context = "\n\n".join([
        f"Document {i+1} (Score: {doc['rrf_score']:.3f}):\ncontext: {doc['content']} \n metadata: {doc['metadata']}"
        for i, doc in enumerate(retrieved_docs)
    ])
    
    # Create prompt for Groq
    prompt = f"""
        You are a helpful AI assistant. Answer the question based on the provided context.

        Context:
        {context}

        Question: {question}

        Instructions:
        - Use only the information from the provided context to answer the question
        - If the context doesn't contain enough information to answer the question don't use your brain to make up answer just say "The provided context does not contain enough information to answer the question."
        - Be concise and accurate
        - Cite relevant information from the context when appropriate
        - don't mention in between that this answer is from source file 1 or 2.
        - After you finish answering the question then you can mention that the answer is reterieved from which source.
        - source is already provided in the context in the metadata section. you can use that to mention the source of answer after you finish answering the question.
        - provide source in this format source: source path 
        Answer:
    """
    
    # Call Groq API
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=GROQ_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )
        
        answer = chat_completion.choices[0].message.content
        return answer.strip()
        
    except Exception as e:
        return f"Error generating answer: {str(e)}"
