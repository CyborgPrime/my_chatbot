# my_basic_web_chatbot.py (chatbot app)

from flask import Flask, render_template, request
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

chatbot_app = Flask(__name__)  # Rename the Flask app instance

@chatbot_app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        prompt = request.form.get("question")

        if prompt.lower() == "quit":
            return render_template("chatbot.html", response="You have quit the conversation.")

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a game master bot. You can create compelling adventures and present them through a text adventure simulator interface."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response = result.choices[0].message.content

        return render_template("chatbot.html", response=response)

    return render_template("chatbot.html", response=None)

if __name__ == "__main__":
    chatbot_app.run(debug=True)  # Use chatbot_app.run() instead of app.run()
