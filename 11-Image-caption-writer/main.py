from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI()

response =client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role" : "user", 
        "content": [
            {"type": "text", "text": "generate a caption for this image in about 50 words"},
            {"type" : "image_url", "image_url": {"url" :"https://images.pexels.com/photos/236599/pexels-photo-236599.jpeg"} }
        ] 
        }
    ]
)
print("🤖 caption: ", response.choices[0].message.content )