from flask import Flask, render_template, request, jsonify, session
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from flask_session import Session  # Import for session-based storage
import os
import openai


app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based sessions
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
# app.config['SESSION_FILE_DIR'] = '/session_data'  # Point to the virtual disk
# app.config['SESSION_FILE_THRESHOLD'] = 500
app.config['SESSION_FILE_DIR'] = '/session_data'  # Point to the mounted disk

openai.api_key = os.getenv("OPENAI_API_KEY")

Session(app)

chat = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', verbose=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    session_id = session.sid  # Get current session ID

    if session_id not in session:
        session[session_id] = []
        session[session_id].append(SystemMessage(content="You are a helpful assistant named Bob."))

    messages = session[session_id]
    user_input = request.form['user_input']
    
    messages.append(HumanMessage(content=user_input))
    ai_response = chat(messages=messages).content
    messages.append(AIMessage(content=ai_response))

    session[session_id] = messages  # Update the session with the new messages

    return jsonify({'ai_response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
