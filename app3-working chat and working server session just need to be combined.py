from flask import Flask, render_template, request, session
from flask_session import Session
import os

# import module dependencies
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)

# Configure Flask-Session to use server-side sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')  # Specify your session file directory
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")

Session(app)

# Define the AI model and parameters
aiModel = "gpt-3.5-turbo"
aiTemperature = 0.6
aiHistory = 20
aiVerbosity = True

# Define the game loop prompt
gameLoopPrompt = "You're a text adventure game simulator in the Traveller RPG's '3rd Imperium' setting, with the user as the main character on a mission from the Imperial Scout Services. Follow the story circle framework, provide interactions with objects and NPCs, and keep responses brief. Offer exit options and describe routes from previous locations. Avoid lengthy paragraphs and don't start responses with 'AI.' Always let the user make decisions, ensuring actions have consequences in the game. For example, when the user says 'Look around,' respond with narrative descriptions that immerse them into the game world and guide them through their mission, such as describing the Imperial Scout Base and its surroundings."

# Define the bot template for the game loop
gameLoopTemplate = """
    {history}
    {combined_input}
    Assistant:
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
    return session.get('history', [])  # Use the list directly



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
        combined_input = f"System: {gameLoopPrompt}\nHuman: {user_input}\n"
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
