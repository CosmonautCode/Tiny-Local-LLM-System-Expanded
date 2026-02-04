
from app.llm.chat import ChatSystem




def main():

    chat = ChatSystem()
    chat.load_agents()
    llm = chat.choose_agent()
    chat.chat_display()

if __name__ == "__main__":
    main()
