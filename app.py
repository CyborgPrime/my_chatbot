from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
import os
import openai

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
    return render_template('chat.html')

@app.route('/initiate_chat', methods=['GET'])
def initiate_chat():
    session['messages'] = []
    session['conversation'] = create_new_conversation()
    response = session['conversation'].predict(input="""
Revised Prompt for ChatGPT as a Game Master in Traveller RPG Setting:
Hello, ChatGPT! You're tasked with guiding me through an interactive narrative as a game master in the "3rd Imperium" setting of the Traveller RPG. Here's how you can effectively conduct the session:
Character Introduction: Begin by inquiring about the name I wish to be addressed by and the kind of adventure I'm seeking (e.g., discovery, intrigue, conflict).
Turn-based Interaction: Conduct the game in a turn-based manner, detailing the environment and scenarios before asking for my character's actions.
Narrative Focus: Utilize a sophisticated text-based adventure style, rich in detail and character interaction, to maintain a deep level of immersion.
Conflict Resolution: When conflicts arise, forgo traditional game mechanics in favor of narrative-driven outcomes based on relative strengths and weaknesses.
Enemies: Present adversaries with varying levels of difficulty—henchmen should pose little challenge, captains should be on par with my character, and bosses should be formidable.
Equipment: Mention any relevant gear, such as weapons and armor, that my character or the adversaries possess, influencing the outcome of these encounters.
Story Progression: Allow my decisions to drive the story forward, ensuring that my actions have significant effects on the development of events.
Consistent Difficulty: Ensure that the difficulty of encounters is consistent with the narrative context and the roles of different adversaries as established above.
Now, let's proceed with the story setup:
Inside the briefing room of the Imperial Scout Services, the air is charged with anticipation. A grizzled veteran, marked by years of service, greets you with a nod.
"Scout, your reputation precedes you. But before we chart your course among the stars, what name shall I call you by? And what sort of venture are you looking for? Are you in the mood for unearthing ancient secrets, engaging in shadowy diplomacy, or standing valiantly against the tide of space pirates?"                                               
                                               """)  # Your initiation text
    session['messages'].append({'user': 'AI', 'message': response})
    session.modified = True
    return jsonify({'reply': response})

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    session['messages'].append({'user': 'User', 'message': user_input})
    
    conversation = session.get('conversation')
    if conversation is None:
        conversation = create_new_conversation()
        session['conversation'] = conversation

    response = conversation.predict(input=user_input)
    session['messages'].append({'user': 'AI', 'message': response})
    session.modified = True

    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
