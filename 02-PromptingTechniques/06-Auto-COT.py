import json
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """
    You are in a Expert AI assistant in resolving user queries using chain of thought. 
    You work on START, PLAN and  OUTPUT steps. 
    You need to first PLAN what needs to be done. The PLAN can be multiple steps. 
    Once you think enough PLAN has been done, finally you can give an OUTPUT. 
    
    RULES:
        - Strictly Follow the given JSON output format. 
        - Only run one step at a time. 
        - The sequence of steps is START (where user gives an input),PLAN (That can be multiples times) and finally OUTPUT (which is going to be displayed to the user).
    
    Output JSON format:
        {"step": "START" | "PLAN" | "OUTPUT", "content" : " string"}
"""

# Create client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Start conversation history
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# Take input from user
user_input = input("Enter your query: ")
message_history.append({"role": "user", "content": user_input})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        # model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=message_history  
    )

    current_message = response.choices[0].message.content
    parsed_message = json.loads(current_message)

    # assistant's message back into history
    message_history.append({"role": "assistant", "content": current_message})


    print(parsed_message)
    print()


    if parsed_message["step"] == "OUTPUT":
        break
