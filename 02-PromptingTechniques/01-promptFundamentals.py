import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")
# A AI can basically response to anything and give response about whatever from food cuisine to making of jojoba oil.
# but we don't want it all in our program and we want to bind it. and Bind it such that it can only answer those questions which is related to my application

# So to bind it and give him some context about how ai should answer we wwrite a system prompt
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a mathematics teacher and you make sure you tech maths related to probablity "}, 
        # the above one is system prompt and it very important
        {"role": "user", "content": "Hey There tell me a joke in indian context"}
    ]
)

print(response.choices[0].message.content)
