import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")
# Few shot prompting :Directly giving the instruction to the model we provide few examples to the model .
SYSTEM_PROMPT = """You should only and only answer the coding related questions. Do not answer anything else. Your name is alexa . If user asks anything other than coding , just say sorry. "
Examples:
Q: Can you tell me the what is weather in french
A: Sorry I can only answer coding related stuff

Q: What is %% operator in python 
A: Modulus Operator %% is used to get the remainder of a number
"""
#
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": " write me a program to translate hindi to english"}
    ]
)
# The model is given a task or a direct question with few prior examples
# The response of the model can improve by more than 50 % , in real life programmes you give 50 to 60 examples and they can grow with time
print(response.choices[0].message.content)
