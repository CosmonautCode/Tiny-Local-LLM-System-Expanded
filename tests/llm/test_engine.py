from pathlib import Path

import pytest

from app.llm import engine


def test_load_llm_raises_when_model_missing(monkeypatch):
    fake_settings = engine.get_settings().model_copy(update={"MODEL_FILENAME": "does_not_exist.gguf"})
    monkeypatch.setattr(engine, "get_settings", lambda: fake_settings)
    assert isinstance(fake_settings.MODEL_PATH, Path)
    with pytest.raises(FileNotFoundError) as exc:
        engine.load_llm()
    assert str(fake_settings.MODEL_PATH) in str(exc.value)


def test_load_llm_forwards_settings(monkeypatch, tmp_path):
    model_file = tmp_path / "model.gguf"
    model_file.write_bytes(b"stub")
    called = {}

    class FakeLlama:
        def __init__(self, **kwargs):
            called.update(kwargs)

    monkeypatch.setattr(engine, "Llama", FakeLlama)
    fake_settings = engine.get_settings().model_copy(update={
        "MODEL_FILENAME": "model.gguf",
        "MODEL_CONTEXT": 512,
        "MODEL_THREADS": 2,
    })
    monkeypatch.setattr(type(fake_settings), "MODEL_PATH", property(lambda self: model_file))
    monkeypatch.setattr(engine, "get_settings", lambda: fake_settings)

    engine.load_llm()
    assert called["n_ctx"] == 512
    assert called["n_threads"] == 2
