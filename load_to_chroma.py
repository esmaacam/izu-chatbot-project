import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()
chroma_client = chromadb.PersistentClient(path="data/chroma_db")

# Koleksiyonu sıfırla
try:
    chroma_client.delete_collection("izu_docs")
except:
    pass
collection = chroma_client.create_collection("izu_docs")

# Klasörleri ve dosyaları işle
folders = ["data/temiz_txt", "data/ders_programlari"]
for folder in folders:
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".txt"):
                # ÖNEMLİ: errors='ignore' ile kodlama hatalarını atlıyoruz
                with open(os.path.join(folder, filename), "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                if len(content) > 10: # Boş dosya değilse
                    embedding = client.embeddings.create(model="text-embedding-3-small", input=content[:8000]).data[0].embedding
                    collection.add(ids=[filename], documents=[content], embeddings=[embedding], metadatas=[{"type": "doc"}])
                    print(f"Yüklendi: {filename}")

# Hoca dosyası
if os.path.exists("tum_hocalar.json"):
    with open("tum_hocalar.json", "r", encoding="utf-8") as f:
        hocalar = json.load(f)
        for i, hoca in enumerate(hocalar):
            hoca_str = json.dumps(hoca, ensure_ascii=False)
            embedding = client.embeddings.create(model="text-embedding-3-small", input=hoca_str[:8000]).data[0].embedding
            collection.add(ids=[f"hoca_{i}"], documents=[hoca_str], embeddings=[embedding], metadatas=[{"type": "hoca"}])
            print(f"Hoca yüklendi: {i}")

print("\n--- İŞLEM TAMAMLANDI: Veritabanı hazır! ---")