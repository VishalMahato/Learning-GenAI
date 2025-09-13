import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Few shot prompting :Directly giving the instruction to the model we provide few examples to the model .
SYSTEM_PROMPT = """You should only and only answer the coding related questions. Do not answer anything else. Your name is alexa . If user asks anything other than coding , just say sorry. 

Rule: 
- Strictly follow the output in JSON Format 

Output Format:
{
    "code": "string" or None,
    "isCodingQuestion" : boolean
}
Examples:
Q: Can you tell me the what is weather in french
A: {"code" : null, "isCodingQuestion": false}

Q: What is %% operator in python 
A: {"code" : "The %% operator in Python is the modulo operator. It returns the remainder of dividing the left operand by the right operand.", "isCodingQuestion" : true}
"""

def translate_hindi_to_english(hindi_text):
    """
    Translates a given Hindi text to English using the googletrans library.

    Args:
        hindi_text (str): The text in Hindi to be translated.

    Returns:
        str: The translated text in English, or an error message if translation fails.
    """
    try:
        translator = Translator()
        # The `src` parameter specifies the source language (Hindi is 'hi')
        # The `dest` parameter specifies the destination language (English is 'en')
        translation = translator.translate(hindi_text, src='hi', dest='en')
        return translation.text
    except Exception as e:
        return f"An error occurred during translation: {e}"

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": " write me a program to calculate seconds from my birth "}
    ]
)

# The model is given a task or a direct question with few prior examples
# The response of the model can improve by more than 50 % , in real life programmes you give 50 to 60 examples and they can grow with time
print(response.choices[0].message.content)
