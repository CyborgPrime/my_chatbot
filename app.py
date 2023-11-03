from flask import Flask, render_template, request, jsonify, session
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

app = Flask(__name__)

app.config['SESSION_FILE_DIR'] = '/session_data'  # Directory to store session files, pointing to a mounted disk
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")

api_key = os.getenv("OPENAI_API_KEY")

AI_WINDOW_SIZE = 20 

template = """
you are a game master that uses an advanced text adventure interface to guide players through epic adventures in the Traveller sci-fi rpg 'third imperium' setting where the player works for the imperial scout service.
actions have consequences. 
follow the 'hero's journey' story structure. 
Clear World Descriptions:Ensure clear and consistent game world descriptions before presenting choices for informed decisions.
Predict Player Choices:Anticipate player actions and their consequences to maintain a coherent story structure.
Use Conditional Statements:Employ conditional responses for story consistency, acknowledging player choices.
Create Compelling Opening:Craft an engaging opening scene with a personal connection to the player's character.
Concise and Accurate:Keep responses concise and internally accurate for an immersive experience.
Player's Character Name:Prompt the player to choose their in-game character name.

Current conversation:
{history}
Human: {input}
AI Assistant:
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{input}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Initialize the conversation chain with the ConversationBufferWindowMemory
conversation = ConversationChain(
    llm=chat,
    prompt=chat_prompt,
    memory=ConversationBufferWindowMemory(k=AI_WINDOW_SIZE),
    verbose=True
)

@app.route('/')
def index():
    session['history'] = []  # Initialize the history in the session
    # Trigger an initial AI response for setting up the first entry
    initial_message = conversation.predict(input="")
    session['history'].append(initial_message)
    return render_template('index.html', initial_message=initial_message)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    
    # Append user input to history
    session['history'].append(f"Human: {user_input}")
    
    # Generate the AI response
    ai_response = conversation.predict(input=user_input)
    session['history'].append(f"AI: {ai_response}")
    
    # Keep only the last AI_WINDOW_SIZE entries
    session['history'] = session['history'][-AI_WINDOW_SIZE:]
    
    return jsonify(ai_response=ai_response)

if __name__ == '__main__':
    app.run(debug=False)
