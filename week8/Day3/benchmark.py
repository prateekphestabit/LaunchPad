from llama_cpp import Llama
import time
import csv
import os

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
QUANTIZED_DIR = "/home/prateek/Prateek/LaunchPad/week8/Day3/quantized"

MODELS = {
    "FP16" : f"{QUANTIZED_DIR}/model-FP16/tinyllama-f16.gguf",
    "INT8" : f"{QUANTIZED_DIR}/model-INT8/tinyllama-q8.gguf",
    "INT4" : f"{QUANTIZED_DIR}/model-INT4/tinyllama-q4.gguf",
}

# Test prompts — one per task type from your dataset
PROMPTS = [
    {
        "id": "qa",
        "text": "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nWhat is compound interest?</s>\n<|assistant|>\n"
    },
    {
        "id": "reasoning",
        "text": "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nA stock was bought at $50 and sold at $70. Dividends received were $5. Calculate the total return percentage.</s>\n<|assistant|>\n"
    },
    {
        "id": "extraction",
        "text": "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nExtract all financial figures from this text: Apple reported Q3 revenue of $81.8B, up 5% YoY, with net income of $19.9B and EPS of $1.26.</s>\n<|assistant|>\n"
    },
]

# ─────────────────────────────────────────
# BENCHMARK FUNCTION
# ─────────────────────────────────────────
def benchmark_model(label, model_path, prompts, n_tokens=150):
    print(f"\n{'='*50}")
    print(f" Testing: {label}")
    print(f"{'='*50}")

    # Get file size
    size_bytes = os.path.getsize(model_path)
    size_gb = size_bytes / (1024 ** 3)

    # Load model
    llm = Llama(
        model_path=model_path,
        n_ctx=512,
        n_threads=os.cpu_count(),   # use all CPU cores
        verbose=False,
    )

    results = []

    for prompt in prompts:
        print(f"\n  Prompt type : {prompt['id']}")

        start = time.time()
        output = llm(
            prompt["text"],
            max_tokens=n_tokens,
            temperature=0.7,
            echo=False,
            stop=["</s>"],
        )
        elapsed = time.time() - start

        tokens_generated = output["usage"]["completion_tokens"]
        tokens_per_sec   = tokens_generated / elapsed if elapsed > 0 else 0
        response_text    = output["choices"][0]["text"].strip()

        print(f"  Tokens/sec  : {tokens_per_sec:.2f}")
        print(f"  Latency     : {elapsed:.2f}s")
        print(f"  Response    : {response_text[:120]}...")

        results.append({
            "model"         : label,
            "size_gb"       : round(size_gb, 2),
            "prompt_type"   : prompt["id"],
            "tokens_per_sec": round(tokens_per_sec, 2),
            "latency_sec"   : round(elapsed, 2),
            "tokens_out"    : tokens_generated,
            "response"      : response_text[:200],
        })

    return results

# ─────────────────────────────────────────
# RUN ALL MODELS
# ─────────────────────────────────────────
all_results = []

for label, path in MODELS.items():
    all_results.extend(benchmark_model(label, path, PROMPTS))

# ─────────────────────────────────────────
# SAVE RESULTS TO CSV
# ─────────────────────────────────────────
os.makedirs("/home/prateek/Prateek/LaunchPad/week8/Day3/benchmarks", exist_ok=True)
CSV_PATH = "/home/prateek/Prateek/LaunchPad/week8/Day3/benchmarks/results.csv"

with open(CSV_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
    writer.writeheader()
    writer.writerows(all_results)

print(f"\nResults saved to {CSV_PATH}")

# ─────────────────────────────────────────
# PRINT SUMMARY TABLE
# ─────────────────────────────────────────
print("\n── SUMMARY ─────────────────────────────────────────")
print(f"{'Model':<8} {'Size(GB)':>10} {'Prompt':>12} {'Tok/sec':>10} {'Latency':>10}")
print("-" * 55)
for r in all_results:
    print(
        f"{r['model']:<8} "
        f"{r['size_gb']:>10} "
        f"{r['prompt_type']:>12} "
        f"{r['tokens_per_sec']:>10} "
        f"{r['latency_sec']:>9}s"
    )