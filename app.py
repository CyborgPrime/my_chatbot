import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def display_env_var():
    env_var = os.environ.get('FLASK_SECRET_KEY', 'Environment variable not set.')
    return f'FLASK_SECRET_KEY: {env_var}'

if __name__ == '__main__':
    app.run(debug=True)
