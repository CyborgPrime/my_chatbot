from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # Import Flask-Session
import os
import secrets  # Import the secrets module
import uuid  # Import the uuid module for generating session IDs

# Import module dependencies
from langchain import LLMChain
from langchain.memory import ConversationBufferWindowMemory

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

# Create the Flask app
app = Flask(__name__)

# Initialize the Flask session with a secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

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

# Define a function to generate a unique session ID
def generate_session_id():
    return str(uuid.uuid4())

# Initialize Flask-Session with your app and SQLAlchemy database
app.config['SESSION_TYPE'] = 'sqlalchemy'

# Initialize the SQLAlchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/vgm_sessions'
db = SQLAlchemy(app)

Session(app)

# Define a model for the session table
class SessionData(db.Model):
    __tablename__ = 'sessions'  # Specify the table name here
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True)
    player_id = db.Column(db.String(255))
    chat_history = db.Column(db.Text)

# Initialize the AI chat model
chatgpt_chain = LLMChain(
    llm=openai.Completion.create,
    prompt=gameLoopTemplate,
    verbose=aiVerbosity,
    memory=ConversationBufferWindowMemory(k=aiHistory),
)

# Initialize the chat history for each session
def init_session_history():
    return []

# Define a function to get the session history
def get_session_history():
    if 'history' not in session:
        session['history'] = init_session_history()
    return session['history']

# Define a function to set the session history
def set_session_history(history):
    session['history'] = history

# Route for the chat interface
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
    with app.app_context():
        db.create_all()  # Create the database table for sessions if it doesn't exist

    app.run(debug=True)
