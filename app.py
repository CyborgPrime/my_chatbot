from flask import Flask, render_template, request
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]
app = Flask(__name__)

# Initialize a list to store the chat history
chat_history = []

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        prompt = request.form.get("question")

        if prompt.lower() == "quit":
            return render_template("chatbot.html", response="You have quit the conversation.")

        # Create a list of message objects for the chat history
        chat_history_messages = [
            {
                "role": "system",
                "content": "You are a game master bot. You can create compelling adventures and present them through a text adventure simulator interface."
            }
        ]

        # Add the user's prompt to the chat history
        chat_history_messages.append({
            "role": "user",
            "content": prompt
        })

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history_messages
        )

        response = result.choices[0].message.content

        # Add the user input and chat response to the chat history
        chat_history.append({"user_input": prompt, "chat_response": response})

        # Keep only the last 5 interactions in the chat history
        if len(chat_history) > 5:
            chat_history.pop(0)

        return render_template("chatbot.html", response=response, chat_history=chat_history)

    return render_template("chatbot.html", response=None, chat_history=[])

if __name__ == "__main__":
    app.run(debug=True)
