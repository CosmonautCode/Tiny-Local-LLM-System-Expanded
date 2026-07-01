from app.config import APP_DIR, get_settings


def test_settings_singleton():
    assert get_settings() is get_settings()


def test_model_path_anchored_to_app_dir():
    settings = get_settings()
    assert settings.MODEL_PATH.parent == APP_DIR / "models"


def test_agents_path_points_to_llm_dir():
    settings = get_settings()
    assert settings.AGENTS_PATH.parent.name == "llm"
    assert settings.AGENTS_PATH.name == settings.AGENTS_FILENAME
