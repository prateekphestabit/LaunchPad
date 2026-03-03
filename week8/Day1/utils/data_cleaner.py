import json
import numpy as np
from transformers import AutoTokenizer

DATA_PATH = "/home/prateek/Prateek/LaunchPad/week8/Day1/data/data.jsonl"
OUTPUT_PATH = "/home/prateek/Prateek/LaunchPad/week8/Day1/data/cleaned.jsonl"

tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

lengths = []
samples = [] 

with open(DATA_PATH, "r") as f:
    for line in f:
        sample = json.loads(line)
        text = sample["instruction"] + sample["input"] + sample["output"]
        tokens = tokenizer(text, truncation=False)["input_ids"]
        lengths.append(len(tokens))
        samples.append((sample, len(tokens)))

## =================Max length to cut of outliers==================
MAX_LENGTH = int(np.percentile(lengths, 95)) 

## =================== remove outliers =====================
filtered_samples = [s for s, l in samples if l <= MAX_LENGTH]

print(f"Original samples: {len(samples)}")
print(f"Filtered samples: {len(filtered_samples)}")

## ================== save filtered samples =====================
with open(OUTPUT_PATH, "w") as f:
    for sample in filtered_samples:
        f.write(json.dumps(sample) + "\n")