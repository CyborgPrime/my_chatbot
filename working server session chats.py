from flask import Flask, request, render_template_string, session, redirect, url_for
import os
from flask_session import Session


app = Flask(__name__)
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)

# Initialize the Flask session with a secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'text_area_content' not in session:
        session['text_area_content'] = ""

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        current_text = session['text_area_content']
        session['text_area_content'] = current_text + "\n" + user_input if current_text else user_input
        return redirect(url_for('index'))

    return render_template_string('''
    <html>
    <body>
        <form method="post">
            User Input: <input type="text" name="user_input"><br>
            <textarea name="text_area" rows="10" cols="50">{{ text_area_content }}</textarea><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    ''', text_area_content=session['text_area_content'])

if __name__ == '__main__':
    app.run(debug=True)
