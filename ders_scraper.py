import tabula
import os
import requests
from bs4 import BeautifulSoup

# Link dosyanı oku
with open("ders_linkleri.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

os.makedirs("data/ders_programlari", exist_ok=True)

for i, url in enumerate(urls):
    dosya_adi = f"data/ders_programlari/program_{i}.txt"
    try:
        # Önce URL'den içeriği çek
        response = requests.get(url, timeout=10)
        
        # İçerik PDF ise tabula kullan
        if 'application/pdf' in response.headers.get('Content-Type', ''):
            # Kodlama hatası almamak için hata ayıklama (ignore) ekledik
            dfs = tabula.read_pdf(url, pages='all', multiple_tables=True, encoding='latin-1')
            text = "\n".join([df.to_string(index=False) for df in dfs])
        else:
            # HTML ise güzelce temizle
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator="\n", strip=True)
            
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Başarılı: program_{i}.txt")
        
    except Exception as e:
        print(f"Hata ({url}): {e}")