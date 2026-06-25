import chromadb

client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="data/chroma_db"
    )
)

collections = client.list_collections()

print("Bulunan koleksiyonlar:")
for c in collections:
    print("-", c.name)
