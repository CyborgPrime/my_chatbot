import os
import openai
 
openai.api_key = os.environ["OPENAI_API_KEY"]

while True:
    prompt = input("Please enter a question or request (type 'quit' to exit):")

    if prompt.lower() == "quit":
        break  # Exit the loop if the user enters "quit"

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("AI: " + result.choices[0].message.content)
