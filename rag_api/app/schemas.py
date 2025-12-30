from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]


class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: list