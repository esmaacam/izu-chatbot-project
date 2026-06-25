import chromadb

# Veritabanına bağlan
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection(name="izu_docs")

# Veritabanında "bilgisayar" geçen dökümanları sorgula
results = collection.get() # Tüm dökümanları çek

print(f"Veritabanında toplam {len(results['documents'])} adet döküman var.")

# İlk 5 dökümanın içeriğine bakalım
for i in range(min(5, len(results['documents']))):
    print(f"\n--- Döküman {i+1} Başlangıcı ---")
    print(results['documents'][i][:200]) # İlk 200 karakter