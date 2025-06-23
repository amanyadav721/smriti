from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from  memory.add import add_memory
from ai.main import chat_bot
app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: list[dict]

class Chat(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Chat API"}


@app.post("/memory/add")
async def chat_endpoint(request: ChatRequest):
    response = add_memory(
        user_id=request.user_id,
        chat_thread=request.message
    )
    return {"response": response}

@app.post("/chat")
async def chat_endpoint(request: Chat):
    if not request.user_id or not request.message:
        raise HTTPException(status_code=400, detail="User ID and message are required")

    response = chat_bot(
        user_id=request.user_id,
        query=request.message
    )
    return {"response": response}


