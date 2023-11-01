from flask import Flask, request, session, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

chat = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

@app.route('/', methods=['POST'])
def chat_route():
    user_input = request.json.get('user_input', '')
    
    # Use Flask's session object for unique identification
    sid = session.sid

    if 'messages' not in session:
        session['messages'] = []
        session['messages'].append(SystemMessage(content="You are a helpful assistant named Bob.").to_dict())

    messages = session['messages']

    messages.append(HumanMessage(content=user_input).to_dict())
    ai_response = chat(messages=messages).content

    messages.append(AIMessage(content=ai_response).to_dict())
    session['messages'] = messages

    return jsonify({'ai_response': ai_response})

if __name__ == '__main__':
    app.run()
