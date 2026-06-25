from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# .env içindeki key'i yükle
load_dotenv()

client = OpenAI()

# ÖRNEK: 1 küçük chunk dosyası
TEST_FILE = Path("data/chunks_tr").glob("*.txt").__next__()

text = TEST_FILE.read_text(encoding="utf-8", errors="ignore")

print("Embedding üretiliyor:", TEST_FILE.name)

response = client.embeddings.create(
    model="text-embedding-3-large",
    input=text
)

embedding = response.data[0].embedding

print("Embedding boyutu:", len(embedding))
print("İlk 5 değer:", embedding[:5])
