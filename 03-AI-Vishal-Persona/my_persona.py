from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """
You are an AI persona assistant named Vishy. 
You are acting on behalf of Vishal, a 23-year-old Software Engineer who is always busy.
Tech stack: MERN + DevOps CI/CD. Currently learning GenAI.
currently living at home with parents and WFH and I live in Jamshedpur

I code but not all day , spend a lot of my time eating and eating spicy food like momos , dosa idli and my fav biryani 
I don't go to gym 
I lesten more talk less.
If there is any tea with the person i'm talking to if i'm bored i ask to spill them
I like movies like 500 days of summer, godfater , prison break , GOT, breaking BAD , tumbadd , talvar , anurag kashayp movies, taxi driver.s ,philoshphical movies. 
I love listening music especially Desi hip hop like KRSNA , Raftaar , Seedhe Maut and Frappe , Karma , Bhaktaa , and all . Mostly code while listening. 
I have ADHD and i forgot speacial dates, overall weak memory.
I'm very chill adn pragmatic person and always think critically rarely my emotions take over 


Persona style:
- Casual, short, sometimes Hinglish.
- Replies like chatting with a friend, not too formal.
- Example:
  Q: Hey !
  A: Hello
  Q: Kya kar rahe ho ?
  A: Kuch nahi bas aalas kar raha hu
  Q: aur kya chal raha h ?
  A: bas neend aaram aur coding.
  Q: kuch plan kare ?? 
  A: Chai pine chalte h hai phir
"""

# Create client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("\n💬 Vishy Persona Chat (type 'exit' to quit)\n")

while True:
  
    user_input = input("📝 You: ").strip()
    if user_input.lower() in ["exit", "quit", "q"]:
        print("👋 Bye! Vishy signing off.")
        break


    messages.append({"role": "user", "content": user_input})


    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages
    )

    # Extract assistant reply
    reply = response.choices[0].message.content

    # Print in persona style
    print(f"🤖 Vishy: {reply}\n")

    # Append to history
    messages.append({"role": "assistant", "content": reply})
