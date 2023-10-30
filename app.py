from flask import Flask, request


app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet_user():
    # Extract the username from the query parameters
    username = request.args.get('username')

    if username:
        # Generate a greeting message
        greeting_message = f"Hello, {username}!"

        # Return the greeting message as a response
        return greeting_message
    else:
        # Handle the case when the username is not provided
        return "Please provide a username as a query parameter.", 400

if __name__ == '__main__':
    app.run(debug=True)
