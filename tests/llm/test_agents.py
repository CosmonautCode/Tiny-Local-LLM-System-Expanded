import json

import pytest

from app.llm import agents as agents_mod
from app.llm.agents import Agent, choose_agent, load_agents


def test_load_agents_reads_configured_file():
    result = load_agents()
    assert len(result) >= 1
    assert all(isinstance(a, Agent) for a in result)
    assert all(a.name and a.system_prompt for a in result)


def test_load_agents_missing_key(monkeypatch, tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"nope": []}), encoding="utf-8")
    fake_settings = agents_mod.get_settings().model_copy()
    monkeypatch.setattr(type(fake_settings), "AGENTS_PATH", property(lambda self: bad))
    monkeypatch.setattr(agents_mod, "get_settings", lambda: fake_settings)
    with pytest.raises(ValueError):
        load_agents()


def test_choose_agent_valid_pick():
    agents = [
        Agent("A", "a", "sp-a"),
        Agent("B", "b", "sp-b"),
    ]
    picked = choose_agent(agents, read_input=lambda _prompt: "2", write=lambda *_a: None)
    assert picked.id == "b"


def test_choose_agent_retries_on_invalid():
    agents = [Agent("A", "a", "sp-a")]
    inputs = iter(["not-a-number", "9", "1"])
    picked = choose_agent(agents, read_input=lambda _p: next(inputs), write=lambda *_a: None)
    assert picked.id == "a"
