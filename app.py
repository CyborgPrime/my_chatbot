from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def run_chatbot():
    # Use subprocess to run the "my_basic_web_chatbot.py" script
    try:
        subprocess.run(["python", "my_basic_web_chatbot.py"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return '<h1 style="color: white;">Hello, Cyber World!</h1>'
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur when running the script
        error_message = f"An error occurred: {e.stderr.decode()}"
        return f'<p style="color: red;">{error_message}</p>'

if __name__ == '__main__':
    app.run(debug=True)
