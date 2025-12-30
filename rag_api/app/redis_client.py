import redis
import json
from sentence_transformers import SentenceTransformer

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def store_document(doc_id: str, content: str):
    embedding = embedder.encode(content).tolist()

    redis_client.hset(
        f"doc:{doc_id}",
        mapping={
            "content": content,
            "embedding": json.dumps(embedding)
        }
    )


def similarity_search(query: str, top_k: int = 3):
    query_embedding = embedder.encode(query)

    results = []

    for key in redis_client.scan_iter("doc:*"):
        data = redis_client.hgetall(key)
        embedding = json.loads(data["embedding"])

        score = sum(q * d for q, d in zip(query_embedding, embedding))
        results.append((score, data["content"]))

    results.sort(reverse=True, key=lambda x: x[0])
    return [content for _, content in results[:top_k]]