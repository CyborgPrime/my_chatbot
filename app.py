# Importing necessary libraries and classes for the Flask application
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session  # Import for handling server-side sessions
from langchain.chat_models import ChatOpenAI  # Import the ChatOpenAI class for AI chat functionality
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
import os
import openai  # OpenAI's API library for Python

# Initializing the Flask application
app = Flask(__name__)

AI_WINDOW_SIZE = 20

# Configuring Flask session management to store session data on the filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")  # Secret key for sessions, retrieved from environment variable
app.config['SESSION_FILE_DIR'] = './session_data'  # Directory to store session files, pointing to a mounted disk

# Setting the OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initializing session management for the app
Session(app)

# Initializing the ChatOpenAI object with zero temperature and specifying the model version
chat = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', verbose=True)
conversation = ConversationChain(
    llm=chat, 
    memory=ConversationBufferWindowMemory(k=AI_WINDOW_SIZE),
    verbose=False
)

# Define a route for the main page which renders the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Define a route that handles the 'ask' POST request to process user input
@app.route('/ask', methods=['POST'])
def ask():
    session_id = session.sid  # Retrieves the session ID unique to each user interaction

    # If this is a new session, initialize the message list and add the initial system message
    if session_id not in session:
        session[session_id] = []
        session[session_id].append(SystemMessage(content="You are a helpful assistant named Bob."))

    messages = session[session_id]  # Retrieve the list of messages associated with the session ID
    user_input = request.form['user_input']  # Get the user input from the submitted form
    
    # Add the human message to the message list
    messages.append(HumanMessage(content=user_input))
    # Generate AI response using the accumulated messages
    ai_response = chat(messages=messages).content
    # Add the AI response to the message list
    messages.append(AIMessage(content=ai_response))

    # Save the updated message list back into the session
    session[session_id] = messages

    # Send the AI response back to the frontend as JSON
    return jsonify({'ai_response': ai_response})

# Run the Flask app with debugging enabled
if __name__ == '__main__':
    app.run(debug=True)
