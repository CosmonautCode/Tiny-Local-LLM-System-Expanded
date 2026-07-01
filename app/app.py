from app.llm.chat import ChatSystem


def main():
    """Entry point: load agents, pick one, run the REPL."""
    chat = ChatSystem()
    chat.load_agents()
    chat.choose_agent()
    chat.chat_display()


if __name__ == "__main__":
    main()
