from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


APP_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Centralized settings for Tiny-Local-LLM-System-Expanded."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="TLLMX_", extra="ignore")

    MODEL_FILENAME: str = "tinyllama-1.1b-chat-v1.0.Q8_0.gguf"
    MODEL_CONTEXT: int = 2048
    MODEL_THREADS: int = 8
    MODEL_VERBOSE: bool = False

    MAX_HISTORY: int = 6
    MAX_TOKENS: int = 1024
    TEMPERATURE: float = 0.2
    TOP_P: float = 0.9
    REPEAT_PENALTY: float = 1.15

    AGENTS_FILENAME: str = "agents.json"

    @property
    def MODEL_PATH(self) -> Path:
        return APP_DIR / "models" / self.MODEL_FILENAME

    @property
    def AGENTS_PATH(self) -> Path:
        return APP_DIR / "llm" / self.AGENTS_FILENAME


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
