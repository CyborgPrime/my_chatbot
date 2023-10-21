# app.py (main app)

from flask import Flask
from my_basic_web_chatbot import app as chatbot_app  # Import the chatbot app

app = Flask(__name__)

# Mount the chatbot app at the root URL ("/")
app.register_blueprint(chatbot_app, url_prefix='/')

@app.route('/')
def main_route():
    return 'Hello from Main App!'

if __name__ == '__main__':
    app.run(debug=True)
