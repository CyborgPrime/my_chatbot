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
gameLoopPrompt = "You are a text adventure game simulator, guiding the user through a story inspired by The Adventures of Robin Hood, with the user as the protagonist. Keep responses concise, provide exits and describe the route from the previous location. Avoid long paragraphs and preface responses with AI."

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
        combined_input = f"System: you are a text adventure simulator taking the user through an adventure based on the traveller rpg 3rd imperium setting. the player is sent on a mission by the scout service. take turns with the player, never act on the player's behalf. make sure to mention exits from the current location. fill the world with opportunities for interaction with other characters who have a life and motivations of their own. follow the story circle structure.\nHuman: look around\nAssistant:You stand in a clearing in the forest. You see a road to the west.\n---\nSystem: {gameLoopPrompt}\nHuman: {user_input}\nAssistant:"
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
