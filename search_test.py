import chromadb
from openai import OpenAI

client = OpenAI()

# 🔴 AYNI PERSISTENT CLIENT
chroma_client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="izu_docs"
)

query = "Burs başvurusu nasıl yapılır?"

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

docs = results.get("documents", [[]])[0]
metas = results.get("metadatas", [[]])[0]

print("🔎 Soru:", query)
print("\n📄 En alakalı metinler:\n")

for i, (doc, meta) in enumerate(zip(docs, metas), 1):
    print(f"--- Sonuç {i} ---")
    print(doc[:800])
    print(f"(Kaynak: {meta.get('file')})\n")
