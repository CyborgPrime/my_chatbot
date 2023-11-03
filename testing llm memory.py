# Importing necessary libraries and classes for the Flask application
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session  # Import for handling server-side sessions

import os

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

# set the size of the memory window
# how many moves back to keep in the message buffer 
AI_WINDOW_SIZE = 20 

# get the API key from the environment variable 
api_key= os.getenv("OPENAI_API_KEY")

# make a chatbot instance
llm = ChatOpenAI(temperature = 0, openai_api_key=api_key)
# make a new chatbot conversation
conversation = ConversationChain(
    llm = llm,
    verbose = True,
    memory = ConversationBufferWindowMemory(k=AI_WINDOW_SIZE)
)

# loop through the conversation
while True:
    user_input = input("User:")
    print(conversation.predict(input=user_input))
