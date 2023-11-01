from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

chat = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

def message_to_dict(message):
    return {'content': message.content, 'name': getattr(message, 'name', None)}

def dict_to_message(message_dict, message_type):
    if message_type == 'SystemMessage':
        return SystemMessage(content=message_dict['content'])
    elif message_type == 'HumanMessage':
        return HumanMessage(content=message_dict['content'])
    elif message_type == 'AIMessage':
        return AIMessage(content=message_dict['content'])

@app.route("/", methods=['GET', 'POST'])
def chat_route():
    if 'messages' not in session:
        session['messages'] = [{'type': 'SystemMessage', 'data': message_to_dict(SystemMessage(content="You are a helpful assistant named Bob."))}]
        
    if request.method == 'POST':
        user_input = request.form['user_input']
        session['messages'].append({'type': 'HumanMessage', 'data': message_to_dict(HumanMessage(content=user_input))})
        messages = [dict_to_message(m['data'], m['type']) for m in session['messages']]
        ai_response = chat.chat(messages=messages).content
        session['messages'].append({'type': 'AIMessage', 'data': message_to_dict(AIMessage(content=ai_response))})
        session.modified = True
        return jsonify({'ai_response': ai_response})

    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)
