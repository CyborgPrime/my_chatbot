from flask import Flask, render_template, request, session
import os

# import module dependencies
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


app = Flask(__name__)

# Initialize the Flask session with a secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

history = []

# Initialize the AI
aiModel = "gpt-3.5-turbo"
aiTemperature = 0.5
aiHistory = 10
aiVerbosity = False

# Define the game loop prompt
gameLoopPrompt = "You are a text adventure game simulator taking the user through a story similar to The Adventures of Robin Hood but with the user as the protagonist. Avoid large blocks of text; be concise and take turns with the user."

# Define the bot template for the game loop
gameLoopTemplate = """
    {history}
    {combined_input}
"""

# Load the variables into the gameLoopTemplate
gameLoopPromptTemplate = PromptTemplate(
    input_variables=["history", "combined_input"],
    template=gameLoopTemplate
)

chatgpt_chain = LLMChain(
    llm=ChatOpenAI(temperature=aiTemperature, model_name=aiModel),
    prompt=gameLoopPromptTemplate,
    verbose=aiVerbosity,
    memory=ConversationBufferWindowMemory(k=aiHistory),
)


@app.route('/', methods=['GET', 'POST'])
def chat():
    global history

    if request.method == 'POST':
        user_input = request.form['user_input']
        combined_input = f"System: {gameLoopPrompt}\nHuman: {user_input}"
        response = chatgpt_chain.predict(
            history="\n".join(history),
            combined_input=combined_input
        )
        history.append(f'User: {user_input}')
        history.append(response)

    return render_template('chat.html', history=history)


if __name__ == '__main__':
    app.run(debug=True)
