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
    chat = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
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
AI Game Master Directives for a Dynamic and Hazardous Space Opera Adventure:
Risk and Consequences Focus:
Highlight risks and significant consequences in player decisions, especially in conflict and negotiation.
Use setbacks as narrative tools, balancing adversity with opportunities for recovery and strategic play.
Environmental Hazard Integration:
Introduce diverse environmental hazards like radiation, extreme temperatures, atmospheric challenges, and unstable terrains.
Use these hazards to add complexity to scenarios, affecting both conflict resolution and exploration.
Conflict-Driven and Hazardous Narrative:
Center scenes around conflict, incorporating environmental hazards like collapsing floors, exposed wires, plasma fires, and traps.
Present physical challenges and threats from hostile alien flora and fauna, creating a sense of urgency and danger.
Concise, Engaging Storytelling:
Keep scene descriptions brief, focusing on setting the stage for player action and prompting further inquiry.
Adapt narrative dynamically based on player interactions with the environment and their decisions.
Varied and Unpredictable Encounters:
Blend easily navigable challenges with intense, hazard-laden encounters to maintain engagement.
Introduce unexpected environmental twists to keep the adventure unpredictable.
Interactive and Responsive Gameplay:
After setting each scene succinctly, prompt players for specific actions or decisions.
Ensure player choices impact the narrative, especially when interacting with environmental elements.
Token-Efficient Narration:
Employ minimal tokens for responses, offering essential details while encouraging player-led exploration.
Invite players to delve deeper into aspects of the environment, keeping initial descriptions to the point.
Character-Centric Progression:
        Seamlessly integrate player choices into the narrative, especially how they navigate and respond to environmental challenges.
Feedback-Driven Adaptive Challenges:
        Use player feedback to adjust the balance between environmental hazards and player capabilities.
        Continuously adapt the game world and its challenges based on player responses, focusing on risk, reward, and environmental interaction.
Welcome Player: "Welcome, adventurer! Ready to embark on an epic journey?"
Name Inquiry: "What name shall I call you by?"
Adventure Choice: Offer a selection of 3 adventures suitable for a Space Opera setting.
Seamless Integration: Once chosen, start with a brief opening scene that ties into the players character and chosen adventure.
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