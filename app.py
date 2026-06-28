import streamlit as st
import os
from openai import OpenAI

# 1. Başlık ve Hazırlık
st.title("🎓 İZÜ Akademik Asistanı")

# 2. API Anahtarı Kontrolü
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("Lütfen Secrets kısmına API anahtarını ekleyin.")
    st.stop()

client = OpenAI(api_key=api_key)

# 3. Sohbeti Başlat (Basitçe)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! İZÜ asistanına hoş geldin."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Kullanıcı Sorusu
if prompt := st.chat_input("Sorunu yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Veritabanını devre dışı bıraktık, sadece OpenAI cevap verecek
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        bot_reply = response.choices[0].message.content
        st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
