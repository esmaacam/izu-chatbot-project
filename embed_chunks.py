import os
import json
from openai import OpenAI

client = OpenAI()

CHUNKS_DIR = "data/chunks"
OUTPUT_FILE = "data/embeddings/embeddings.json"

os.makedirs("data/embeddings", exist_ok=True)


def create_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def process_chunks():
    embeddings_data = []

    for filename in os.listdir(CHUNKS_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(CHUNKS_DIR, filename)

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            embedding = create_embedding(text)

            embeddings_data.append({
                "chunk": filename,
                "text": text,
                "embedding": embedding
            })

            print("Embedding oluşturuldu:", filename)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings_data, f)

    print("Tüm embeddingler kaydedildi.")


if __name__ == "__main__":
    process_chunks()