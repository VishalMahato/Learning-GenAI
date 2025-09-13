import json
from dotenv import load_dotenv
import os
from openai import OpenAI
#  if you ever use any thinking model they use a COT prompting technique.
# We want a model to answer more precise then it should think
#

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
# Note -- IF there is no gap of a line between rules and the above sentence then it's not works -VVI
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)
# we are manually adding all the code of the COT in the messages list

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey write a code to add n numbers "},
        {"role": "assistant", "content": json.dumps({"step": "START", "content": "Hey write a code to add n numbers"})},
        {"role": "assistant", "content": json.dumps({"step": "PLAN","content": "The user wants a code to add 'n' numbers. I should provide a solution in a common programming language like Python."})}
        {"role": "assistant", "content": json.dumps({"step": "PLAN","content": "The user wants a code to add 'n' numbers. I should provide a solution in a common programming language like Python."})}

    ]
)

print(response.choices[0].message.content)
