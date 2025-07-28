from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import json
from rapidfuzz import process
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("faq.json") as f:
    faq_data: Dict[str, str] = json.load(f)

openai.api_key = os.getenv("OPENAI_API_KEY")  # Store key in .env

class Message(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def find_answer(user_input: str) -> str | None:
    questions = list(faq_data.keys())
    match, score, _ = process.extractOne(user_input, questions, score_cutoff=60)
    if match:
        return faq_data[match]
    return None

def ask_openai(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return "Sorry, I couldn't process that right now."

@app.post("/chat", response_model=ChatResponse)
async def chat(msg: Message) -> ChatResponse:
    faq_answer = find_answer(msg.message)
    if faq_answer:
        return ChatResponse(response=faq_answer)
    
    # Fallback to OpenAI for non-DevOps or generic questions
    gpt_reply = ask_openai(msg.message)
    return ChatResponse(response=gpt_reply)
