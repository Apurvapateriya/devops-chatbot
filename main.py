from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import json
from rapidfuzz import fuzz

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAQ data
with open("faq.json") as f:
    faq_data: Dict[str, str] = json.load(f)

class Message(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def find_answer(user_input: str) -> str:
    user_input = user_input.lower().strip()
    best_score = 0
    best_match = None

    for question in faq_data:
        score = fuzz.token_set_ratio(user_input, question.lower())
        if score > best_score:
            best_score = score
            best_match = question

    if best_score >= 60:  # Adjust threshold if needed
        return faq_data[best_match]

    return "I'm not sure. Please check with the DevOps team."

@app.post("/chat", response_model=ChatResponse)
async def chat(msg: Message) -> ChatResponse:
    answer = find_answer(msg.message)
    return ChatResponse(response=answer)
