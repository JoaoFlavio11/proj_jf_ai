import httpx
from app.redis_client import similarity_search

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

async def generate_answer(question: str):
  context_docs = similarity_search(question)

  context = "\n\n".join(context_docs)

  prompt = f"""
    Você é o NeuronAI.

    Use o contexto abaixo para responder a pergunta.
    Se o contexto não for suficiente, responda com seu conhecimento geral.

    Contexto:
    {context}

    Pergunta:
    {question}
  """
  async with httpx.AsyncClient() as client:
    response = await client.post(
      OLLAMA_URL,
      json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
      }
    )
    
  return response.json()["response"]