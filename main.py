from __future__ import annotations
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import json
import difflib
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-username.github.io"],  # Replace with your actual GitHub Pages URL
    allow_methods=["POST"],  # Only allow POST requests
    allow_headers=["*"],
)

with open("faq.json") as f:
    faq_data: Dict[str, str] = json.load(f)

class Message(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# 🧠 Fuzzy
def find_answer(user_input: str) -> str:
    user_input = user_input.lower().strip()
    questions = list(faq_data.keys())
    close_matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)
    if close_matches:
        best_match = close_matches[0]
        return faq_data[best_match]
    return "I'm not sure. Please check with the DevOps team."

# 🤖 Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(
    msg: Message,
    x_api_key: Optional[str] = Header(None)
) -> ChatResponse:
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    answer = find_answer(msg.message)
    return ChatResponse(response=answer)
