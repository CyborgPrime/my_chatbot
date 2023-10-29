from flask import Flask, render_template, request
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
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
                    "content": """The Virtual Game Master project is an exciting blend of AI-driven storytelling and interactive role-playing. As an end user, you can expect:
    Immersive Adventures: Dive into captivating narratives and explore diverse scenarios, crafting your destiny within the game world.
    Endless Variety: Enjoy unique adventures every time you play, thanks to AI's ability to generate diverse storylines, characters, and settings.
    Solo RPG Experience: Experience the thrill of solo role-playing, allowing you to play on your own schedule, 24/7.
    Craft Your Story: Customize your character, choose genres, and influence the plot, ensuring every adventure feels uniquely yours.
    Community Interaction: Join a welcoming community of fellow adventurers, share your creations, and participate in events.
    Always Evolving: The project is in constant development, with regular updates and new features to enhance your gaming experience.
    Support and Feedback: Your feedback is valued and helps shape the project's future. Join us on Discord, Facebook, YouTube, or Patreon to get involved! this project was created and programmed by Santa Fe-based entrepreneur Frank Succardi (aka CyborgPrime) is a digital artist, multimedia producer, game designer, tech consultant, and author of over 20 RPG-related publications, including Realm Crafter User’s Guide, as well as the What’s Wrong With The Ship series, and the Humanoid Resources Dept series.
With over three decades of producing compelling original content for a variety of popular sci-fi RPG systems, Frank creates imaginative expansions for the enjoyment of players and Game Masters alike.
Frank holds a degree in Digital Media, hosts RPG games at sci-fi conventions, produces content for virtual tabletop systems, and runs a YouTube channel and a Facebook group dedicated to sci-fi gaming enthusiasts. He publishes under the CyborgPrime Publishing label.
Frank works from home at the base of the Rocky Mountains in New Mexico, occupying his spare time in volunteer service to various non-profits and enjoying his time with his wife and dogs. Frank enjoys playing video games, creating art, programming, and writing new games."""
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
    app.run(debug=True)  
