import uuid
import time
import logging
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from model_loader import get_model
from config import (
    DEFAULT_TEMP, DEFAULT_TOP_K, DEFAULT_TOP_P,
    MAX_TOKENS, SYSTEM_PROMPT
)

# ─────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TinyLlama Local API",
    description="Local LLM API powered by TinyLlama Q4 GGUF",
    version="1.0.0",
)

# ─────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# ─────────────────────────────────────────
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = MAX_TOKENS
    temperature: Optional[float] = DEFAULT_TEMP
    top_k: Optional[int] = DEFAULT_TOP_K
    top_p: Optional[float] = DEFAULT_TOP_P
    stream: Optional[bool] = False

class GenerateResponse(BaseModel):
    request_id: str
    response: str
    tokens_generated: int
    time_taken_sec: float
    tokens_per_sec: float

class Message(BaseModel):
    role: str      # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    max_tokens: Optional[int] = MAX_TOKENS
    temperature: Optional[float] = DEFAULT_TEMP
    top_k: Optional[int] = DEFAULT_TOP_K
    top_p: Optional[float] = DEFAULT_TOP_P
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    request_id: str
    response: str
    tokens_generated: int
    time_taken_sec: float
    tokens_per_sec: float

# ─────────────────────────────────────────
# HELPER — Build TinyLlama prompt
# ─────────────────────────────────────────
def build_chat_prompt(messages: List[Message]) -> str:
    prompt = f"<|system|>\n{SYSTEM_PROMPT}</s>\n"
    for msg in messages:
        if msg.role == "user":
            prompt += f"<|user|>\n{msg.content}</s>\n"
        elif msg.role == "assistant":
            prompt += f"<|assistant|>\n{msg.content}</s>\n"
    prompt += "<|assistant|>\n"   # signal model to respond
    return prompt

# ─────────────────────────────────────────
# STARTUP — preload model
# ─────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up — loading model into memory...")
    get_model()
    logger.info("Model ready!")

# ─────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "model": "TinyLlama Q4 GGUF"}

# ─────────────────────────────────────────
# POST /generate — single prompt
# ─────────────────────────────────────────
@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] /generate | prompt: {req.prompt[:60]}...")

    model = get_model()

    # Format prompt with TinyLlama template
    prompt = (
        f"<|system|>\n{SYSTEM_PROMPT}</s>\n"
        f"<|user|>\n{req.prompt}</s>\n"
        f"<|assistant|>\n"
    )

    # Streaming response
    if req.stream:
        def stream_tokens():
            output = model(
                prompt,
                max_tokens=req.max_tokens,
                temperature=req.temperature,
                top_k=req.top_k,
                top_p=req.top_p,
                stream=True,
                stop=["</s>"],
            )
            for chunk in output:
                token = chunk["choices"][0]["text"]
                yield token

        return StreamingResponse(stream_tokens(), media_type="text/plain")

    # Normal response
    start = time.time()
    output = model(
        prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_k=req.top_k,
        top_p=req.top_p,
        stop=["</s>"],
        echo=False,
    )
    elapsed = time.time() - start

    response_text  = output["choices"][0]["text"].strip()
    tokens_out     = output["usage"]["completion_tokens"]
    tokens_per_sec = round(tokens_out / elapsed, 2) if elapsed > 0 else 0

    logger.info(f"[{request_id}] Done | {tokens_out} tokens | {elapsed:.2f}s | {tokens_per_sec} tok/s")

    return GenerateResponse(
        request_id=request_id,
        response=response_text,
        tokens_generated=tokens_out,
        time_taken_sec=round(elapsed, 2),
        tokens_per_sec=tokens_per_sec,
    )

# ─────────────────────────────────────────
# POST /chat — multi-turn conversation
# ─────────────────────────────────────────
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] /chat | turns: {len(req.messages)}")

    model   = get_model()
    prompt  = build_chat_prompt(req.messages)

    # Streaming response
    if req.stream:
        def stream_tokens():
            output = model(
                prompt,
                max_tokens=req.max_tokens,
                temperature=req.temperature,
                top_k=req.top_k,
                top_p=req.top_p,
                stream=True,
                stop=["</s>"],
            )
            for chunk in output:
                token = chunk["choices"][0]["text"]
                yield token

        return StreamingResponse(stream_tokens(), media_type="text/plain")

    # Normal response
    start = time.time()
    output = model(
        prompt,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_k=req.top_k,
        top_p=req.top_p,
        stop=["</s>"],
        echo=False,
    )
    elapsed = time.time() - start

    response_text  = output["choices"][0]["text"].strip()
    tokens_out     = output["usage"]["completion_tokens"]
    tokens_per_sec = round(tokens_out / elapsed, 2) if elapsed > 0 else 0

    logger.info(f"[{request_id}] Done | {tokens_out} tokens | {elapsed:.2f}s | {tokens_per_sec} tok/s")

    return ChatResponse(
        request_id=request_id,
        response=response_text,
        tokens_generated=tokens_out,
        time_taken_sec=round(elapsed, 2),
        tokens_per_sec=tokens_per_sec,
    )