import streamlit as st
import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasını yükle (yerelde çalışır, sunucuda etkisi yoktur)
load_dotenv()

# Streamlit Arayüzü - Hata olsa bile önce başlığı gösterelim
st.title("🎓 İZÜ Akademik Asistanı")

try:
    # 1. API Bağlantısı
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("API Anahtarı bulunamadı! Lütfen Secrets kısmına OPENAI_API_KEY ekleyin.")
        st.stop()
    
    client = OpenAI(api_key=api_key)

    # 2. Veritabanı Yolu
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")
    
    # 3. Veritabanı Bağlantısı
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    # Koleksiyonu kontrol et
    collections = chroma_client.list_collections()
    if len(collections) > 0:
        collection = chroma_client.get_collection(collections[0].name)
    else:
        collection = chroma_client.create_collection("izu_bilgileri")

    # 4. Sohbet Arayüzü
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Merhaba! İZÜ ile ilgili sorularını yanıtlayabilirim."}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Sorunuzu buraya yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Vektör araması (Hata yakalama ekledik)
            try:
                results = collection.query(query_texts=[prompt], n_results=1)
                context = results["documents"][0][0] if results["documents"] else ""
            except:
                context = ""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sen bir İZÜ asistanısın. Bağlamı kullanarak cevap ver."},
                    {"role": "user", "content": f"Bağlam: {context}\nSoru: {prompt}"}
                ]
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

except Exception as e:
    st.error(f"Uygulama Hatası: {e}")
