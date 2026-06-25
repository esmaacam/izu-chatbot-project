import requests
from bs4 import BeautifulSoup
from pathlib import Path

SAVE_DIR = Path("data/html")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

def clean_and_save(url):
    print("İndiriliyor:", url)

    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.text, "lxml")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    filename = url.replace("https://", "").replace("/", "_") + ".txt"
    (SAVE_DIR / filename).write_text(text, encoding="utf-8")

with open("urls.txt", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    clean_and_save(url)

print("Tüm sayfalar indirildi.")
