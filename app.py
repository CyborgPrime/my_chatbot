from flask import Flask, render_template, request, session
from flask_session import Session
import os
import redis

# Import module dependencies
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)

# Initialize the Flask session with a secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Configure Flask-Session to use Redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # This is recommended for better security
app.config['SESSION_KEY_PREFIX'] = 'vGM_AcE'  # Change this to a unique prefix

# Initialize the Flask-Session extension
Session(app)

# Define the AI model and parameters
aiModel = "gpt-3.5-turbo"
aiTemperature = 0.2
aiHistory = 20
aiVerbosity = True

# Define the game loop prompt
gameLoopPrompt = "You are a text adventure game simulator taking the user through a story similar to The Adventures of Robin Hood but with the user as the protagonist. Avoid large blocks of text; be concise and take turns with the user. At each new location, be sure to specify the exits and the route the player took from the previous location. Do not preface your response with AI:"

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
    if request.method == 'POST':
        user_input = request.form['user_input']
        combined_input = f"System: {gameLoopPrompt}\nHuman: {user_input}"
        history = session.get('history', [])  # Retrieve the chat history from the session

        response = chatgpt_chain.predict(
            history=history,
            combined_input=combined_input
        )

        history.append(f'User: {user_input}')
        history.append(response)

        # Store the updated chat history back in the session
        session['history'] = history

    else:
        # If it's a GET request, initialize an empty chat history in the session
        session['history'] = []

    return render_template('chat.html', history=session['history'])

if __name__ == '__main__':
    app.run(debug=True)
