from fastapi import FastAPI,Body
from ollama import Client



app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def read_root():
    return({"hello":"world"})

@app.post("/chat")
def chat(
    message: str = Body( ...,description="The Message")
):
    response =client.chat(model="qwen3:0.6b", messages=[
        {"role" : "user" , "content" :message}
    ]) 
    return {"response" : response.message.content}