import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
chroma_client = chromadb.PersistentClient(path="data/chroma_db")

# Koleksiyonu hata vermeden yakalamak için en güvenli yol
collections = chroma_client.list_collections()
if not collections:
    print("HATA: Veritabanında döküman bulunamadı! Lütfen yükleme (load_to_chroma.py) işlemini yapın.")
    exit()
collection = chroma_client.get_collection(collections[0].name)

def ask_question(question, lang):
    # Dil seçimine göre arama sorgusunu optimize ediyoruz
    embedding = client.embeddings.create(model="text-embedding-3-small", input=question).data[0].embedding
    results = collection.query(query_embeddings=[embedding], n_results=10)
    
    # Eğer veri yoksa boş string döndür
    context = "\n---\n".join(results["documents"][0]) if results["documents"] and results["documents"][0] else ""

    prompt = f"""
    Sen İstanbul Sabahattin Zaim Üniversitesi (İZÜ) akademik asistanısın.
    Kullanıcının seçtiği dil: {lang}
    
    Talimatlar:
    1. Cevabını SADECE {lang} dilinde ver.
    2. BİLGİLER'i kullan. Bilgi yoksa, {lang} dilinde "Kayıt bulunamadı" anlamında bir mesaj ver.
    3. Ders programı sorulursa: Ders kodu, ders adı, AKTS sütunlarını içeren liste/tablo yap.
    4. Toplama yapma, sadece listele.

    BİLGİLER:
    {context}
    
    SORU: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # DİL SEÇENEKLERİ
    print("İZÜ Asistanı başlatıldı.")
    choice = input("Lütfen dil seçin / Please select language (TR/EN): ").upper()
    lang_mode = "Türkçe" if choice == "TR" else "English"
    print(f"\nMod seçildi: {lang_mode}. Çıkmak için 'q'.")
    
    while True:
        q = input(f"\nSoru ({lang_mode}): ")
        if q.lower() == 'q': break
        
        # Seçilen dili ve soruyu gönderiyoruz
        print("\nCevap:", ask_question(q, lang_mode))