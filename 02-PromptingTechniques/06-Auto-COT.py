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
        
    Example:
    START: Hey, Can you solve 2+3*5 / 10
    PLAN: :{STEP: "PLAN" , "content": "SEEMS like user is interested in math problem "}
    PLAN: :{STEP: "PLAN" , "content" : "Looking at the problem , we should solve this using BODMAS method" }
    PLAN: :{STEP: "PLAN" , "content": "Yes BODMAS is the correct thing to be done here " }
    PLAN: :{STEP: "PLAN" , "content":  "first we multiply 3*5 which is 15 " }
    PLAN: :{STEP: "PLAN" , "content": "Now the Equation is 2+15 /10" }
    PLAN: :{STEP: "PLAN" , "content": "Now we must perform divide  15/10 which is 1.5" }
    PLAN: :{STEP: "PLAN" , "content": " now the eqn looks like 2 +1.5" }
    PLAN: :{STEP: "PLAN" , "content": "Finally Lets perform the add 2+15 =3.5!! " }
    PLAN: :{STEP: "PLAN" , "content": " Finally we solved the eqn and left with 3.5 as ans" }
    OUTPUT: :{STEP: "OUTPUT" , "content": " The ans to 2+3*5 /10 is 3.5 " }

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
