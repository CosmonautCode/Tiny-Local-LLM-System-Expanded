import json
from dataclasses import dataclass

from app.config import get_settings


@dataclass(frozen=True)
class Agent:
    """A persona: (display name, id, system prompt)."""

    name: str
    id: str
    system_prompt: str


def load_agents() -> list[Agent]:
    """Read the agent catalog from the configured JSON file."""
    path = get_settings().AGENTS_PATH
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "agents" not in data:
        raise ValueError(f"Agents file missing 'agents' key: {path}")
    return [Agent(name=a["name"], id=a["id"], system_prompt=a["system_prompt"]) for a in data["agents"]]


def choose_agent(agents: list[Agent], read_input=input, write=print) -> Agent:
    """Prompt the user to pick an agent from the list. Loops until a valid choice."""
    write("Select an Agent to chat with:")
    for i, agent in enumerate(agents):
        write(f"{i + 1}. {agent.name}")
    while True:
        try:
            choice = int(read_input("Enter number: ")) - 1
        except ValueError:
            write("Please enter a number.")
            continue
        if 0 <= choice < len(agents):
            return agents[choice]
        write("Invalid choice. Try again.")
