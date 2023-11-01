from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate

from langchain.schema import AIMessage, HumanMessage, SystemMessage

chat = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

messages = [
    SystemMessage(content="You are a helpful assistant named Bob.")
]

while True:
    user_input = input("Player:")
    messages.append(HumanMessage(content=user_input))
    ai_reponse = chat(messages=messages).content
    print("ai:",ai_reponse)
    messages.append(AIMessage(content=ai_reponse))