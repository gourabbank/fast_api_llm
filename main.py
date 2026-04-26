import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"Hello": "World"}