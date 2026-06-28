import streamlit as st
import chromadb
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasını yükle (yerel çalışmalar için)
load_dotenv()

# 1. OpenAI Bağlantısı (Secrets'tan veya Environment Variable'dan otomatik çeker)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 2. Veritabanı Yolu (Sunucu için tam adresleme)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

# 3. Güvenli Veritabanı Bağlantısı
chroma_client = chromadb.PersistentClient(path=DB_PATH)

# Koleksiyonu güvenli bir şekilde al veya oluştur
try:
    collections = chroma_client.list_collections()
    if len(collections) > 0:
        collection = chroma_client.get_collection(collections[0].name)
    else:
        # Koleksiyon hiç yoksa hata verme, yeni oluştur
        collection = chroma_client.create_collection("izu_bilgileri")
except Exception as e:
    st.error(f"Veritabanı bağlantı hatası: {e}")
    # Hata durumunda kodun çökmemesi için boş bir nesne
    collection = None
