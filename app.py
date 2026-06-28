import streamlit as st
import chromadb
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. AYARLAR
load_dotenv()
# Streamlit Cloud'daki 'Secrets' kısmından anahtarı okur
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 2. VERİTABANI BAĞLANTISI (Sunucu uyumlu yol)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")
chroma_client = chromadb.PersistentClient(path=DB_PATH)

# Koleksiyonu al veya oluştur
try:
    collections = chroma_client.list_collections()
    if len(collections) > 0:
        collection = chroma_client.get_collection(collections[0].name)
    else:
        collection = chroma_client.create_collection("izu_bilgileri")
except Exception as e:
    st.error(f"Veritabanı hatası: {e}")
    collection = None

# 3. YARDIMCI FONKSİYON
def ask_question(question):
    # Basit bir vektör arama simülasyonu
    results = collection.query(query_texts=[question], n_results=2)
    context = "\n".join(results["documents"][0]) if results["documents"] else ""
    
    prompt = f"Bağlam: {context}\nSoru: {question}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 4. ARAYÜZ (Ekranı çizen kısım)
st.title("🎓 İZÜ Akademik Asistanı")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Size nasıl yardımcı olabilirim?"}]

# Geçmiş mesajları yazdır
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if collection is not None:
            response = ask_question(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error("Veritabanına ulaşılamadı!")
