import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
client = OpenAI()


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages =[
        {"role": "user", "content" : "Hey There"}
    ]
)

print(response.choices[0].message.content)