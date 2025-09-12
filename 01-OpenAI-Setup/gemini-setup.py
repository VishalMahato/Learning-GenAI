import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(
    api_key=GEMINI_API_KEY
)


response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words in 100 words"
)
print(response.text)

