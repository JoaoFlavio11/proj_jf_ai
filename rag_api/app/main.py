from fastapi import FastAPI
from app.schemas import ChatRequest
from app.rag import generate_answer
import uuid

app = FastAPI(title="NeuronAI RAG API")

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
  question = request.messages[-1].content
  answer = await generate_answer(question)

  return{
    "id": str(uuid.uuid4()),
    "object": "chat.completion",
    "choices": [
      {
        "index": 0,
        "message": {
        "role": "assistant",
        "content": answer
        },
        "finish_reason": "stop"
      }
    ]
  }