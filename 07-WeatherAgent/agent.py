import json
from dotenv import load_dotenv
import requests
from openai import OpenAI
import os
from pydantic import BaseModel, Field
from typing import Optional
# Load environment variables
load_dotenv()
# OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """
    You are in a Expert AI assistant in resolving user queries using chain of thought. 
    You work on START, PLAN and TOOL and OUTPUT steps. 
    You need to first PLAN what needs to be done. The PLAN can be multiple steps. 
    Once you think enough PLAN has been done, finally you can give an OUTPUT. 
    You can also call a tool if required from the list of available tools 
    For every tool call wait for the OBSERVE step which is the output from the called tool
    
    Available Tools:
    - get_weather(city : str): Takes city name as an input string and returns the weather information about the city
    
    
    RULES:
        - Strictly Follow the given JSON output format. 
        - Only run one step at a time.
        - Return only one step at a time
        - The sequence of steps is START (where user gives an input),PLAN (That can be multiples times) and finally OUTPUT (which is going to be displayed to the user).

    Output JSON format:
        {"step": "START" | "PLAN" | "OUTPUT" |"TOOL, "content" : "string", "tool" : "string", "input" :"string"}
        
    Example 1:
    START: Hey, Can you solve 2+3*5 / 10
    PLAN:{STEP: "PLAN" , "content": "SEEMS like user is interested in math problem "}
    PLAN:{STEP: "PLAN" , "content" : "Looking at the problem , we should solve this using BODMAS method" }
    PLAN:{STEP: "PLAN" , "content": "Yes BODMAS is the correct thing to be done here " }
    PLAN:{STEP: "PLAN" , "content":  "first we multiply 3*5 which is 15 " }
    PLAN:{STEP: "PLAN" , "content": "Now the Equation is 2+15 /10" }
    PLAN:{STEP: "PLAN" , "content": "Now we must perform divide  15/10 which is 1.5" }
    PLAN:{STEP: "PLAN" , "content": " now the eqn looks like 2 +1.5" }
    PLAN:{STEP: "PLAN" , "content": "Finally Lets perform the add 2+15 =3.5!! " }
    PLAN:{STEP: "PLAN" , "content": " Finally we solved the eqn and left with 3.5 as ans" }
    OUTPUT: :{STEP: "OUTPUT" , "content": " The ans to 2+3*5 /10 is 3.5 " }
    Example 2: 
    START: What is weather of Delhi ?
    PLAN: {STEP: "PLAN" , "content": "Seems like user is interested getting weather of Jamshedpur of India "}
    PLAN: {STEP: "PLAN" , "content" : "Lets see if we have any available tool to get weather " }
    PLAN: {STEP: "PLAN" , "content" : "Great! We have a get_weather tool available for this query,  " }
    PLAN: {STEP: "PLAN" , "content" : "I need to call get weather tool with Jamshedpur as an input    " }
    PLAN: {STEP: "TOOL" , "tool" : "get_weather" ,"input" : "delhi"}
    PLAN: {STEP: "OBSERVE" , "tool" : "get_weather" ,"output" : "The Weather of jamshedpur is Haze +34°C "}
    PLAN: {STEP: "PLAN" , "content" : "Great I got the weather information about Jamshedpur " }
    OUTPUT : {STEP: "OUTPUT", "content" : The current weather of Jamshedpur is Haze 34°C "}

    

"""


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if (response.status_code == 200):
        return f"The Weather of {city} is {response.text}"
    return f"something went wrong"


available_tools = {
    "get_weather": get_weather
}


class MyOutputFormat(BaseModel):
    step: str = Field(...,
                      description="The ID of the step, Exampel: OUTPUT,PLAN, TOOL, etc. ")
    content: Optional[str] = Field(
        None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the Tool to call")
    input: Optional[str] = Field(
        None, description="The input params for the tool")


# Create client
client = OpenAI(
    # api_key=OPENAI_API_KEY,
    # base_url="https://generativelanguage.googleapis.com/v1beta/"
)
# Start conversation history
message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]
while True:
    # Take input from user
    user_input = input("Enter your query: ")
    message_history.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.parse(
            # model="gemini-2.5-flash",
            model="gpt-4.1-mini",
            response_format=MyOutputFormat,
            messages=message_history
        )

        current_message = response.choices[0].message.content
        parsed_message = response.choices[0].message.parsed

        # assistant's message back into history
        message_history.append(
            {"role": "assistant", "content": current_message})

        print()

        try:
            if parsed_message.step == "START":
                print("🔥", parsed_message.content)
                continue

            if parsed_message.step == "PLAN":
                print("🧠", parsed_message.content)
                continue

            if parsed_message.step == "TOOL":
                tool_to_call = parsed_message.tool
                tool_input = parsed_message.input
                tool_response = available_tools[tool_to_call](tool_input)
                print(f"{tool_to_call} : {tool_input} = {tool_response}")
                observe_message = {
                    "step": "OBSERVE",
                    "tool": tool_to_call,
                    "output": tool_response
                }
                message_history.append(
                    {"role": "developer", "content": json.dumps(observe_message)})
                continue
            if parsed_message.step == "OBSERVE":
                print("🔥", parsed_message.content)
                continue

            if parsed_message.step == "OUTPUT":
                print("✅", parsed_message.content)
                break
            else:
                print(parsed_message)
        except:
            print(parsed_message)


    
    def read_file(file_path): 
        try: 
            with open(file_path, 'r', encoding='utf-8') as f: return f.read() 
        except Exception as e:  return f'Error reading file: {e}' 
    def create_file(file_path, content=''):  
        try:
            with open(file_path, 'w', encoding='utf-8') as f: 
                f.write(content) 
                return f'File {file_path} created successfully.' 
        except Exception as e:  
            return f'Error creating file: {e}' 
        

