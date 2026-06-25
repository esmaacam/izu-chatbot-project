import os
import re

# Klasör yollarını mutlak (tam) yol olarak tanımlayalım
BASE_DIR = os.getcwd()
INPUT_DIR = os.path.join(BASE_DIR, "data", "clean_txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "temiz_txt")

print(f"Burası aranıyor: {INPUT_DIR}")

if not os.path.exists(INPUT_DIR):
    print("HATA: 'data/clean_txt' klasörü bulunamadı! Dosyalar nerede?")
else:
    dosyalar = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
    print(f"Bulunan dosya sayısı: {len(dosyalar)}")

    for dosya_adi in dosyalar:
        yol = os.path.join(INPUT_DIR, dosya_adi)
        with open(yol, "r", encoding="utf-8") as f:
            metin = f.read()
        
        # Temizleme
        yeni_metin = re.sub(r'[^a-zA-ZçÇğĞıİöÖşŞüÜ0-9\s.,?!-]', '', metin)
        yeni_metin = re.sub(r'\s+', ' ', yeni_metin)
        
        with open(os.path.join(OUTPUT_DIR, dosya_adi), "w", encoding="utf-8") as f:
            f.write(yeni_metin)
        
        print(f"Başarıyla temizlendi: {dosya_adi}")