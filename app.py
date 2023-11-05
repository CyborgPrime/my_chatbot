from flask import Flask, render_template, request, jsonify, session, make_response
from flask_session import Session
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
import os
import openai
import json

app = Flask(__name__)

AI_WINDOW_SIZE = 20

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
app.config['SESSION_FILE_DIR'] = '/session_data'

openai.api_key = os.getenv("OPENAI_API_KEY")

Session(app)

# Function to create a new conversation object for a session
def create_new_conversation():
    chat = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', verbose=True)
    conversation = ConversationChain(
        llm=chat, 
        memory=ConversationBufferWindowMemory(k=AI_WINDOW_SIZE),
        verbose=True
    )
    return conversation

@app.route('/')
def home():
    if 'messages' not in session:
        session['messages'] = []
    # Check if chat history cookie exists
    chat_history = request.cookies.get('chat_history')
    if chat_history:
        # Parse and load chat history from the cookie
        session['messages'] = json.loads(chat_history)
    return render_template('chat.html')

@app.route('/initiate_chat', methods=['GET'])
def initiate_chat():
    session['messages'] = []
    # Create a new conversation for this session
    session['conversation'] = create_new_conversation()
    response = session['conversation'].predict(input="")
    session['messages'].append({'user': 'AI', 'message': response})
    session.modified = True
    return jsonify({'reply': response})

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    session['messages'].append({'user': 'User', 'message': user_input})
    
    # Retrieve the conversation object for this session
    conversation = session.get('conversation')
    if conversation is None:
        # Create a new conversation if it doesn't exist (shouldn't happen)
        conversation = create_new_conversation()
        session['conversation'] = conversation

    response = conversation.predict(input=user_input)
    session['messages'].append({'user': 'AI', 'message': response})
    session.modified = True

    # Store chat history in a cookie
    response = jsonify({'reply': response})
    chat_history_cookie = json.dumps(session['messages'])
    response.set_cookie('chat_history', chat_history_cookie)

    return response

if __name__ == '__main__':
    app.run(debug=True)
