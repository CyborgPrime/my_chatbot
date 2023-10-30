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

# Define the AI model and parameters
aiModel = "gpt-3.5-turbo"
aiTemperature = 0.2
aiHistory = 20
aiVerbosity = True

# Define the game loop prompt
gameLoopPrompt = "You are a text adventure game simulator taking the user through a story similar to The Adventures of Robin Hood but with the user as the protagonist. Avoid large blocks of text; be concise and take turns with the user. At each new location, be sure to specify the exits and the route the player took frm the previous location. Do not preface your response with AI:"

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

# Initialize the chat history for each session
def init_session_history():
    return []

def get_session_history():
    if 'history' not in session:
        session['history'] = init_session_history()
    return session['history']

def set_session_history(history):
    session['history'] = history

chatgpt_chain = LLMChain(
    llm=ChatOpenAI(temperature=aiTemperature, model_name=aiModel),
    prompt=gameLoopPromptTemplate,
    verbose=aiVerbosity,
    memory=ConversationBufferWindowMemory(k=aiHistory),
)

@app.route('/', methods=['GET', 'POST'])
def chat():
    history = get_session_history()

    if request.method == 'POST':
        user_input = request.form['user_input']
        combined_input = f"System: {gameLoopPrompt}\nHuman: {user_input}"
        response = chatgpt_chain.predict(
            history=history,
            combined_input=combined_input
        )
        history.append(f'User: {user_input}')
        history.append(response)

        # Update the user's chat history in the session
        set_session_history(history)

    return render_template('chat.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
