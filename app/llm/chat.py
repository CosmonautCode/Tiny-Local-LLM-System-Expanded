from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.status import Status
import json

from pathlib import Path
from app.llm.engine import load_multiple_instances

console = Console()
MAX_HISTORY = 6

class ChatSystem:
    def __init__(self):
        self.history = []
        self.llm_instances = {}
        self.llm = None
        self.system_prompt = None

    def load_agents(self):

        base_dir = Path(__file__).parent
        agents_path = base_dir / "agents.json"

        with open(agents_path, "r") as f:
            self.agent_config = json.load(f)["agents"]
            

        self.llm_instances = load_multiple_instances(3)  # list

    def choose_agent(self):
        print("Select an Agent to chat with:")

        for i, agent in enumerate(self.agent_config):
            print(f"{i + 1}. {agent['name']}")

        while True:
            try:
                choice = int(input("Enter number: ")) - 1
                if 0 <= choice < len(self.agent_config):
                    break
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")

        self.llm = self.llm_instances[choice]
        self.system_prompt = self.agent_config[choice]["system_prompt"]

        return self.llm


    def chat_display(self):
        console.clear()
        console.rule("[bold blue] Tiny Local LLM Chat Expanded[/bold blue]", style="bold blue")

        console.print(Panel.fit(
            "[bold green]Local LLM ready![/bold green]\n Type [bold yellow] 'exit' [/bold yellow] to quit",
            title = "[bold cyan] Status [/bold cyan]",
            border_style="green"
        ))

        console.print(Panel.fit(
            "[bold magenta]Welcome![/bold magenta]\nYou can start chatting with your Tiny LLM below.",
            border_style="magenta"
        ))

        while True:
            user_input = console.input("[bold cyan]You > [/bold cyan] ")

            if user_input.lower() in {"exit", "quit"}:
                console.print("[bold red]Exiting... Goodbye![/bold red]")
                break

            self.history.append(("user", user_input))

            messages = [{"role": "system", "content": self.system_prompt}]
            messages += [{"role": role, "content": text} for role, text in self.history]

            with console.status(
                "[bold magenta]LLM is typing...[/bold magenta]",
                spinner="dots"
            ):
                
                output = self.llm.create_chat_completion(
                    messages=messages,
                    max_tokens=1028,
                    temperature=0.2,
                    top_p=0.9,
                    repeat_penalty=1.15,
                )

            response = output["choices"][0]["message"]["content"].strip()
            self.history.append(("assistant", response))


            # Keep history concise
            if len(self.history) > MAX_HISTORY:
                del self.history[:-MAX_HISTORY]

            console.print(
                Panel(
                    Text(response, style="bold magenta"),
                    title="[bold green]LLM[/bold green]",
                    border_style="cyan"
                )
            )
