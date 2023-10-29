from flask import Flask, render_template, request, session
import os

# import module dependencies
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI

app = Flask(__name__)

# Initialize the Flask session with a secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Initialize the AI
aiModel = "gpt-3.5-turbo"
aiTemperature = 0.5
aiHistory = 10
aiVerbosity = False

# Define the game loop prompt
gameLoopPrompt = "You are a text adventure game simulator taking the user through a story similar to The Adventures of Robin Hood but with the user as the protagonist. Avoid large blocks of text; be concise and take turns with the user."

# Initialize a dictionary to store chat histories for different user sessions
chat_histories = {}

# Define a function to get or initialize the chat history for a session
def get_or_initialize_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

# ... Other code ...

@app.route('/', methods=['GET', 'POST'])
def chat():
    # Get the user's session ID
    session_id = session.get('session_id', None)

    # Get or generate a session ID if it doesn't exist
    if session_id is None:
        session_id = str(hash(request.remote_addr + str(time.time())))
        session['session_id'] = session_id

    # Get or initialize the chat history for this session
    history = get_or_initialize_history(session_id)

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
