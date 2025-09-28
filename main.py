import os
from dotenv import load_dotenv
from langchain_gigachat import GigaChat
from langchain_core.language_models import LanguageModelLike
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


class LLMAgent:
    def __init__(self, model: LanguageModelLike):
        self.model = model
        self.workflow = ...

def main():
    agent = GigaChat(credentials=os.getenv("GIGACHAT_API_KEY"),verify_ssl_certs=False)

    messages = [
        SystemMessage(content="Ты обычный бот, который просто отвечает на сообщения")
    ]
    while True:
        user_input = input("Ты:")
        messages.append(HumanMessage(content=user_input))
        result = agent.invoke(messages)
        print("Gigachat:",result.content)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Пока")
