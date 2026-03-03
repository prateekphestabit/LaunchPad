# QUANTISATION-REPORT.md

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

