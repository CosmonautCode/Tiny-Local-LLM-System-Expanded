
from llama_cpp import Llama
from pathlib import Path

MODEL_PATH = Path("app/models/tinyllama-1.1b-chat-v1.0.Q8_0.gguf")

def load_multiple_instances(n_instances=2):
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    return [
        Llama(model_path=str(MODEL_PATH), n_ctx=2048, n_threads=8, verbose=False)
        for _ in range(n_instances)
    ]

