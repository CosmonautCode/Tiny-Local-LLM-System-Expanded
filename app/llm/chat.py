from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from app.config import get_settings
from app.llm.agents import Agent, choose_agent, load_agents
from app.llm.engine import load_llm


console = Console()


class ChatSystem:
    """REPL that binds a chosen Agent to a single Llama instance."""

    def __init__(self):
        self.settings = get_settings()
        self.agents: list[Agent] = []
        self.agent: Agent | None = None
        self.llm = None
        self.history: list[tuple[str, str]] = []

    def load_agents(self):
        self.agents = load_agents()

    def choose_agent(self):
        self.agent = choose_agent(self.agents)
        self.llm = load_llm()

    def _render_banner(self):
        console.clear()
        console.rule("[bold blue] Tiny Local LLM Chat Expanded[/bold blue]", style="bold blue")
        console.print(Panel.fit(
            "[bold green]Local LLM ready![/bold green]\n Type [bold yellow] 'exit' [/bold yellow] to quit",
            title="[bold cyan] Status [/bold cyan]",
            border_style="green",
        ))
        console.print(Panel.fit(
            "[bold magenta]Welcome![/bold magenta]\nYou can start chatting with your Tiny LLM below.",
            border_style="magenta",
        ))

    def _run_turn(self, user_input: str) -> str:
        self.history.append(("user", user_input))
        messages = [{"role": "system", "content": self.agent.system_prompt}]
        messages += [{"role": role, "content": text} for role, text in self.history]
        with console.status("[bold magenta]LLM is typing...[/bold magenta]", spinner="dots"):
            output = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=self.settings.MAX_TOKENS,
                temperature=self.settings.TEMPERATURE,
                top_p=self.settings.TOP_P,
                repeat_penalty=self.settings.REPEAT_PENALTY,
            )
        response = output["choices"][0]["message"]["content"].strip()
        self.history.append(("assistant", response))
        self._trim_history()
        return response

    def _trim_history(self):
        max_h = self.settings.MAX_HISTORY
        if len(self.history) > max_h:
            # Keep pairs aligned so the trimmed history starts with a user turn.
            drop = len(self.history) - max_h
            if drop % 2:
                drop += 1
            del self.history[:drop]

    def chat_display(self):
        """Run the interactive chat loop for the chosen agent."""
        self._render_banner()
        while True:
            user_input = console.input("[bold cyan]You > [/bold cyan] ")
            if not user_input.strip():
                continue
            if user_input.lower() in {"exit", "quit"}:
                console.print("[bold red]Exiting... Goodbye![/bold red]")
                break
            response = self._run_turn(user_input)
            console.print(Panel(
                Text(response, style="bold magenta"),
                title=f"[bold green]{self.agent.name}[/bold green]",
                border_style="cyan",
            ))
