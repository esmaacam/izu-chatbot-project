import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasındaki API anahtarını yükle
load_dotenv()
openai_client = OpenAI()

# Chroma veritabanına bağlan
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collection = chroma_client.get_collection(name="izu_docs")

# Silinmesini istediğin eski linkler
eski_linkler = [
    "https://www.izu.edu.tr",
    "https://www.izu.edu.tr/ogrenci",
    "https://www.izu.edu.tr/erasmus",
    "https://www.izu.edu.tr/ogrenci-isleri",
    "https://www.izu.edu.tr/akademik-takvim"
]

print("Eski linkler temizleniyor, lütfen bekleyin...\n")

for link in eski_linkler:
    try:
        # 1. Link metnini OpenAI ile 1536 boyutlu vektöre çeviriyoruz
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=link
        )
        link_embedding = response.data[0].embedding

        # 2. Doğru boyuttaki vektörle Chroma'da arama yapıyoruz
        results = collection.query(
            query_embeddings=[link_embedding],
            n_results=15  # O linkin geçebileceği tahmini parça sayısı
        )
        
        # 3. Bulunan dökümanların ID'lerini alıp siliyoruz
        if results and results['ids'] and results['ids'][0]:
            ids_to_delete = results['ids'][0]
            collection.delete(ids=ids_to_delete)
            print(f"Başarıyla Silindi: '{link}' içeren {len(ids_to_delete)} adet parça.")
        else:
            print(f"Bulunamadı veya zaten temizlenmiş: '{link}'")
            
    except Exception as e:
        print(f"'{link}' silinirken bir hata oluştu: {e}")

print("\nİşlem tamamlandı! Hocaların bilgileri güvende, eski linkler temizlendi.")