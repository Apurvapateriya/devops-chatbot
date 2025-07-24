from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import json

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("faq.json") as f:
    faq_data: Dict[str, str] = json.load(f)

class Message(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def find_answer(user_input: str) -> str:
    user_input = user_input.lower().strip()
    for question, answer in faq_data.items():
        if question in user_input:
            return answer
    return "I'm not sure. Please check with the DevOps team."

@app.post("/chat", response_model=ChatResponse)
async def chat(msg: Message) -> ChatResponse:
    answer = find_answer(msg.message)
    return ChatResponse(response=answer)
