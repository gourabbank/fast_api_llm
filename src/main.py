import os
from fastapi import FastAPI,Request
from pydantic import BaseModel
from dotenv import load_dotenv

from src.auth.throttling import apply_rate_limiting

from .ai.gemini import Gemini


load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str="hello"

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"API": "is Running"}

def load_system_prompt():
    try:
        with open("src/prompts/system_prompts.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()

gemini_api_key = os.getenv("GEMINI_API_KEY")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str



@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req:Request):
    ip_address = req.client.host
    apply_rate_limiting(ip_address)  # Replace with actual user IP retrieval logic
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)