from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1 style="color: white;">Hello, Cyber World!</h1>'
