import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import os

# Ayarlar
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="data/chroma_db")

collections = chroma_client.list_collections()

if not collections:
    st.error("Veritabanı bulunamadı. data/chroma_db klasörü boş ya da GitHub'a yüklenmemiş.")
    st.stop()

collection = chroma_client.get_collection(collections[0].name)
