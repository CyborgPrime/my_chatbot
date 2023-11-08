from flask import Flask, render_template, request, jsonify
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Flask app setup
app = Flask(__name__)

# Environment variable for OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# AI Window Size - Number of moves the AI remembers
AI_WINDOW_SIZE = 20

template = """
You are a helpful bot named Bob.

Current conversation:
{history}
Human: {input}
AI Assistant:
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template="{input}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


# Initialize ChatOpenAI with the desired model
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Initialize ConversationChain with the appropriate parameters
conversation = ConversationChain(
    llm=chat, 
    prompt=chat_prompt, 
    memory=ConversationBufferWindowMemory(k=AI_WINDOW_SIZE),
    verbose=True
)

@app.route('/')
def home():
    # Render the chat interface
    return render_template('chat.html')

@app.route('/initiate_chat', methods=['GET'])
def initiate_chat():
    # Trigger initial AI response with empty user input
    response = conversation.predict(input="")
    return jsonify({'reply': response})

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = conversation.predict(input=user_input)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
