import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def display_env_var():
    env_var = os.environ.get('PYTHON_VERSION', 'Environment variable not set.')
    return f'PYTHON_VERSION: {env_var}'

if __name__ == '__main__':
    app.run(debug=True)
