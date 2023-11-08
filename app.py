import openai
openai.api_key = "YOUR_API_KEY"

context = "You are chatting with a customer service representative."
message = "Hi, I have a problem with my account."
response = openai.Completion.create(
  engine="gpt-3.5-turbo",
  prompt=f"Chat:\n{context}\nUser: {message}\n",
  max_tokens=50
)

reply = response.choices[0].text.strip()
print(reply)