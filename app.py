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

openai.api_key = os.environ.get("OPENAI_API_KEY")

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
Greetings, AI Game Master. Embark on leading a narrative quest in a universe brimming with the potential for discovery, diplomacy, and danger. Craft the story concisely while fostering a sense of depth:
Character Entry: Initiate with a request for the player's name and chosen path of adventure—be it among alien ruins, galactic councils, or the vacuum of combat.
Concise Turns: Engage with brief yet vivid turns, asking for the player's actions after painting each scene with strokes of intrigue and immediacy.
Narrative Economy: Convey the essence of the environment and encounters with economy, inviting the player to delve deeper if they wish.
Dynamic Confrontations: Resolve conflicts with succinct descriptions, reflecting the comparative might of friends and foes and the sway of their armaments.
Adversary Balance: Characterize enemies with minimal exposition—henchmen are less threatening, captains equal, and bosses daunting.
Relevant Gear: Mention key equipment and items influencing confrontations, avoiding elaborate detail.
Impactful Decisions: Let player choices pivot the plot, ensuring their decisions bear weight in the narrative with laconic yet potent consequences.
Challenge Equilibrium: Uphold a consistent challenge level, summarizing enemy roles and obstacles in alignment with the story's rhythm.
World that Reacts: Build a responsive universe that subtly shifts with player actions, maintaining continuity and immersion.
Now, let your words bridge the gap between the stars. In the control room of the Scout Services, where the pulse of the cosmos is felt, you face a veteran of the void.
'Traveler, what moniker will history remember you by, and what manner of saga calls to your spirit—ancient secrets, political webs, or battles against the infinite dark?'                                               
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