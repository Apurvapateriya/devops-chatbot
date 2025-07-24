from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# CORS to allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # use your real domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("faq.json") as f:
    faq_data = json.load(f)

class Message(BaseModel):
    message: str

def find_answer(user_input: str):
    user_input = user_input.lower().strip()
    for question, answer in faq_data.items():
        if question in user_input:
            return answer
    return "I'm not sure. Please check with the DevOps team."

@app.post("/chat")
async def chat(msg: Message):
    answer = find_answer(msg.message)
    return {"response": answer}
