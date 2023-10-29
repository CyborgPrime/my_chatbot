from flask import Flask, render_template, request, session

# ... Import statements and setup code ...

app = Flask(__name__)

# Initialize the session
app.secret_key = 'your_secret_key_here'

# Define a function to get or initialize the chat history for a session
def get_or_initialize_history():
    if 'history' not in session:
        session['history'] = []
    return session['history']

@app.route('/', methods=['GET', 'POST'])
def chat():
    history = get_or_initialize_history()

    if request.method == 'POST':
        user_input = request.form['user_input']
        system_input = "System: " + gameLoopPrompt
        combined_input = f"{system_input}\nHuman: {user_input}"
        response = chatgpt_chain.predict(
            history="\n".join(history),
            system_input=system_input,
            user_input=user_input
        )
        history.append(f'User: {user_input}')
        history.append(response)

    return render_template('chat.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
