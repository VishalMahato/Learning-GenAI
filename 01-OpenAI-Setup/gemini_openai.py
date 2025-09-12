import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")
# OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Hey There tell me a joke in indian context"}
    ]
)

print(response.choices[0].message.content)
