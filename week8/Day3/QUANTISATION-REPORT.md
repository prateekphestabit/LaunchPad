# flow
LoRA adapters + Base Model
        ↓
Merge into one full model       
        ↓
Save as FP16                   
        ↓
Convert to GGUF                
        ↓
Quantise GGUF to Q4_0 / Q8_0   
        ↓
Benchmark all formats         



# Clone and build llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make                        # CPU build



# Inside llama.cpp directory
# f16 ==> convert merged model .tensor to .gguf
python convert_hf_to_gguf.py \
    /home/prateek/Prateek/LaunchPad/week8/Day3/merged_model \
    --outfile /home/prateek/Prateek/LaunchPad/week8/Day3/quantized/model-FP16/tinyllama-f16.gguf \
    --outtype f16

# Int 8
./llama-quantize \
    /home/prateek/Prateek/LaunchPad/week8/Day3/quantized/model-FP16/tinyllama-f16.gguf \
    /home/prateek/Prateek/LaunchPad/week8/Day3/quantized/model-INT8/tinyllama-q8.gguf \
    Q8_0

# Int 4
./llama-quantize \
    /home/prateek/Prateek/LaunchPad/week8/Day3/quantized/model-FP16/tinyllama-f16.gguf \
    /home/prateek/Prateek/LaunchPad/week8/Day3/quantized/model-INT4/tinyllama-q4.gguf \
    Q4_0



# QUANTISATION-REPORT

## Model: TinyLlama 1.1B (Fine-tuned)

## File Sizes
| Format | Size   |
|--------|--------|
| FP16   | 2.1 GB |
| INT8   | 1.1 GB |
| INT4   | 608 MB |

## Speed Benchmark (tokens/sec)
| Format | QA  | Reasoning | Extraction | Avg |
|--------|-----|-----------|------------|-----|
| FP16   |12.18|   9.12    |   12.17    |11.36|
| INT8   |22.99|  12.16    |   18.84    |17.99|
| INT4   |36.23|  23.48    |   21.88    |81.59|

