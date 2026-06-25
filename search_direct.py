import chromadb
from openai import OpenAI

client = OpenAI()

chroma_client = chromadb.Client()
collection = chroma_client.get_collection(name="izu_docs")


def rerank(query, documents):

    prompt = f"""
Aşağıdaki belgeleri soruya göre en alakalıdan en alakasız olana sırala.

Soru:
{query}

Belgeler:
{documents}

Sadece sıralanmış belge numaralarını yaz.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def search(query):

    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    docs = results["documents"][0]

    order = rerank(query, docs)

    return docs[:3]


if __name__ == "__main__":
    question = input("Soru sor: ")
    print(search(question))