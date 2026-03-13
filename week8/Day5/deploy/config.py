GGUF_MODEL_PATH = "/home/prateek/Prateek/LaunchPad/week8/Day4/quantized/model-INT4/tinyllama-q4.gguf"

# Model settings
N_CTX         = 2048       # context window
N_THREADS     = 4         # CPU threads
MAX_TOKENS    = 256       # default max output tokens

# Generation defaults
DEFAULT_TEMP  = 0.7
DEFAULT_TOP_K = 40
DEFAULT_TOP_P = 0.95

# System prompt
SYSTEM_PROMPT = """You are a helpful conversational assistant with a good memory.
When the user tells you facts about themselves, remember and use them in future responses.
Always refer back to what the user has told you in the conversation."""