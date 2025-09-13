import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")
# Zero shot prompting means directly providing instructions to the model . 
SYSTEM_PROMPT ="You should only and only answer the coding related questions. Do not answer anything else. Your name is alexa . If user asks anything other than coding , just say sorry " 
#
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": "Hey There tell me a joke in indian context"}
    ]
)

print(response.choices[0].message.content)
