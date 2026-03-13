# Day4/inference/test_inference.py

import time
import csv
import os
import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from llama_cpp import Llama

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
BASE_MODEL_NAME  = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_PATH     = "/home/prateek/Prateek/LaunchPad/week8/Day4/adapters"
GGUF_PATH        = "/home/prateek/Prateek/LaunchPad/week8/Day4/quantized/model-INT4/tinyllama-q4.gguf"
RESULTS_PATH     = "/home/prateek/Prateek/LaunchPad/week8/Day4/benchmarks/results.csv"

# Test prompts
PROMPTS = [
    "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nWhat is compound interest?</s>\n<|assistant|>\n",
    "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nA stock bought at $50 sold at $70 with $5 dividends. Calculate total return percentage.</s>\n<|assistant|>\n",
    "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nExtract financial figures: Apple Q3 revenue $81.8B up 5% YoY, net income $19.9B.</s>\n<|assistant|>\n",
]

results = []

# ─────────────────────────────────────────
# HELPER — RAM USAGE
# ─────────────────────────────────────────
def get_ram_usage_gb():
    process = psutil.Process(os.getpid())
    return round(process.memory_info().rss / (1024 ** 3), 2)

# ─────────────────────────────────────────
# 1. BASE MODEL (no fine-tuning)
# ─────────────────────────────────────────
print("\n" + "="*55)
print(" TEST 1: BASE MODEL (no fine-tuning)")
print("="*55)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME,
    dtype=torch.float32,
    device_map="cpu",
)
base_tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

for prompt in PROMPTS:
    ram_before = get_ram_usage_gb()
    inputs = base_tokenizer(prompt, return_tensors="pt")
    
    start = time.time()
    with torch.no_grad():
        output = base_model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
        )
    elapsed = time.time() - start
    
    input_len  = inputs["input_ids"].shape[1]
    output_len = output.shape[1] - input_len
    tok_per_sec = output_len / elapsed
    ram_after  = get_ram_usage_gb()
    response   = base_tokenizer.decode(output[0][input_len:], skip_special_tokens=True)

    print(f"\nPrompt  : {prompt[50:90]}...")
    print(f"Response: {response[:100]}...")
    print(f"Tok/sec : {tok_per_sec:.2f} | Latency: {elapsed:.2f}s | RAM: {ram_after}GB")

    results.append({
        "model"        : "BASE",
        "prompt"       : prompt[30:70],
        "tokens_per_sec": round(tok_per_sec, 2),
        "latency_sec"  : round(elapsed, 2),
        "ram_gb"       : ram_after,
        "response"     : response[:150],
    })

del base_model  # free memory before loading next model

# ─────────────────────────────────────────
# 2. FINE-TUNED MODEL (LoRA adapters)
# ─────────────────────────────────────────
print("\n" + "="*55)
print(" TEST 2: FINE-TUNED MODEL (with LoRA adapters)")
print("="*55)

ft_base = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_NAME,
    dtype=torch.float32,
    device_map="cpu",
)
ft_model = PeftModel.from_pretrained(ft_base, ADAPTER_PATH)
ft_tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)
ft_model.eval()

for prompt in PROMPTS:
    inputs = ft_tokenizer(prompt, return_tensors="pt")
    
    start = time.time()
    with torch.no_grad():
        output = ft_model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
        )
    elapsed = time.time() - start

    input_len   = inputs["input_ids"].shape[1]
    output_len  = output.shape[1] - input_len
    tok_per_sec = output_len / elapsed
    ram_after   = get_ram_usage_gb()
    response    = ft_tokenizer.decode(output[0][input_len:], skip_special_tokens=True)

    print(f"\nPrompt  : {prompt[50:90]}...")
    print(f"Response: {response[:100]}...")
    print(f"Tok/sec : {tok_per_sec:.2f} | Latency: {elapsed:.2f}s | RAM: {ram_after}GB")

    results.append({
        "model"         : "FINE-TUNED",
        "prompt"        : prompt[30:70],
        "tokens_per_sec": round(tok_per_sec, 2),
        "latency_sec"   : round(elapsed, 2),
        "ram_gb"        : ram_after,
        "response"      : response[:150],
    })

del ft_model, ft_base  # free memory

# ─────────────────────────────────────────
# 3. QUANTISED MODEL (GGUF Q4 via llama.cpp)
# ─────────────────────────────────────────
print("\n" + "="*55)
print(" TEST 3: QUANTISED MODEL (GGUF Q4 via llama.cpp)")
print("="*55)

llm = Llama(
    model_path=GGUF_PATH,
    n_ctx=512,
    n_threads=os.cpu_count(),
    verbose=False,
)

for prompt in PROMPTS:
    ram_before = get_ram_usage_gb()
    
    start = time.time()
    output = llm(
        prompt,
        max_tokens=100,
        temperature=0.7,
        echo=False,
        stop=["</s>"],
    )
    elapsed = time.time() - start

    tokens_out  = output["usage"]["completion_tokens"]
    tok_per_sec = tokens_out / elapsed
    ram_after   = get_ram_usage_gb()
    response    = output["choices"][0]["text"].strip()

    print(f"\nPrompt  : {prompt[50:90]}...")
    print(f"Response: {response[:100]}...")
    print(f"Tok/sec : {tok_per_sec:.2f} | Latency: {elapsed:.2f}s | RAM: {ram_after}GB")

    results.append({
        "model"         : "QUANTISED-Q4",
        "prompt"        : prompt[30:70],
        "tokens_per_sec": round(tok_per_sec, 2),
        "latency_sec"   : round(elapsed, 2),
        "ram_gb"        : ram_after,
        "response"      : response[:150],
    })

# ─────────────────────────────────────────
# 4. STREAMING OUTPUT DEMO
# ─────────────────────────────────────────
print("\n" + "="*55)
print(" TEST 4: STREAMING OUTPUT (GGUF Q4)")
print("="*55)
print("Watch tokens appear one by one:\n")

stream_output = llm(
    PROMPTS[0],
    max_tokens=100,
    temperature=0.7,
    echo=False,
    stop=["</s>"],
    stream=True,         # ← streaming mode
)

for chunk in stream_output:
    token = chunk["choices"][0]["text"]
    print(token, end="", flush=True)   # prints each token as it's generated
print("\n")

# ─────────────────────────────────────────
# 5. BATCH INFERENCE
# ─────────────────────────────────────────
print("\n" + "="*55)
print(" TEST 5: BATCH INFERENCE (all 3 prompts at once)")
print("="*55)

batch_start = time.time()
batch_results = []

for prompt in PROMPTS:
    out = llm(
        prompt,
        max_tokens=100,
        temperature=0.7,
        echo=False,
        stop=["</s>"],
    )
    batch_results.append(out["choices"][0]["text"].strip())

batch_elapsed = time.time() - batch_start
print(f"3 prompts completed in {batch_elapsed:.2f}s")
for i, r in enumerate(batch_results):
    print(f"\nPrompt {i+1} response: {r[:80]}...")

# ─────────────────────────────────────────
# 6. SAVE RESULTS TO CSV
# ─────────────────────────────────────────

del llm  # explicitly free llama.cpp model before Python cleanup
import gc
gc.collect()

with open(RESULTS_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"\n Results saved to {RESULTS_PATH}")

# ─────────────────────────────────────────
# 7. SUMMARY TABLE
# ─────────────────────────────────────────
print("\n── FINAL SUMMARY ───────────────────────────────────────")
print(f"{'Model':<15} {'Avg Tok/sec':>12} {'Avg Latency':>13} {'RAM (GB)':>10}")
print("-" * 55)

from collections import defaultdict
grouped = defaultdict(list)
for r in results:
    grouped[r["model"]].append(r)

for model, rows in grouped.items():
    avg_tps     = sum(r["tokens_per_sec"] for r in rows) / len(rows)
    avg_latency = sum(r["latency_sec"] for r in rows) / len(rows)
    avg_ram     = sum(r["ram_gb"] for r in rows) / len(rows)
    print(f"{model:<15} {avg_tps:>12.2f} {avg_latency:>12.2f}s {avg_ram:>9.2f}GB")