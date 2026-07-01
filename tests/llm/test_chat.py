from app.llm.agents import Agent
from app.llm.chat import ChatSystem


class FakeLLM:
    def __init__(self, response="hello"):
        self.response = response
        self.calls = []

    def create_chat_completion(self, **kwargs):
        self.calls.append(kwargs)
        return {"choices": [{"message": {"content": self.response}}]}


def _chat_with(response="hi"):
    chat = ChatSystem()
    chat.agent = Agent("A", "a", "system-prompt")
    chat.llm = FakeLLM(response)
    return chat


def test_run_turn_updates_history_and_returns_response():
    chat = _chat_with("hi there")
    assert chat._run_turn("hey") == "hi there"
    assert chat.history == [("user", "hey"), ("assistant", "hi there")]


def test_history_trim_keeps_pair_alignment():
    chat = _chat_with("r")
    for i in range(chat.settings.MAX_HISTORY * 2):
        chat._run_turn(f"q{i}")
    assert len(chat.history) <= chat.settings.MAX_HISTORY
    assert chat.history[0][0] == "user"


def test_sampling_params_forwarded_from_settings():
    chat = _chat_with("r")
    chat._run_turn("q")
    call = chat.llm.calls[0]
    assert call["max_tokens"] == chat.settings.MAX_TOKENS
    assert call["temperature"] == chat.settings.TEMPERATURE
    assert call["top_p"] == chat.settings.TOP_P
    assert call["repeat_penalty"] == chat.settings.REPEAT_PENALTY
