from llama_cpp import Llama

from app.config import get_settings


def load_llm() -> Llama:
    """Load one Llama instance using centralized settings."""
    settings = get_settings()
    model_path = settings.MODEL_PATH
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    return Llama(
        model_path=str(model_path),
        n_ctx=settings.MODEL_CONTEXT,
        n_threads=settings.MODEL_THREADS,
        verbose=settings.MODEL_VERBOSE,
    )
