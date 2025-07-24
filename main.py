from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import json
import difflib
import os

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAQ data using absolute path (Render-safe)
faq_path = os.path.join(os.path.dirname(__file__), "faq.json")
with open(faq_path) as f:
    faq_data: Dict[str, str] = json.load(f)

class Message(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def find_answer(user_input: str) -> str:
    user_input = user_input.lower().strip()
    questions = list(faq_data.keys())

    # Use fuzzy matching to find the closest question
    close_matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)
    
    # Debugging logs (visible in Render logs)
    print("User input:", user_input)
    print("Matched:", close_matches)

    if close_matches:
        best_match = close_matches[0]
        return faq_data[best_match]
    return "I'm not sure. Please check with the DevOps team."

@app.post("/chat", response_model=ChatResponse)
async def chat(msg: Message) -> ChatResponse:
    answer = find_answer(msg.message)
    return ChatResponse(response=answer)
