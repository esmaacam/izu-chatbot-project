import os
import re

INPUT_DIR = "data/html"
OUTPUT_DIR = "data/clean_txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Silmek istediğimiz gereksiz kelimeler
BLACKLIST = [
    "ANASAYFA",
    "Menu",
    "FOOTER",
    "LINK",
    "https://",
    "Tüm Hakları Saklıdır",
    "Copyright"
]

def clean_text(content):

    # 1️⃣ Garip karakterleri temizle
    content = re.sub(r"[^\x00-\x7FğüşöçıİĞÜŞÖÇ\s.,:;/()-]", "", content)

    # 2️⃣ Fazla boşlukları temizle
    content = re.sub(r"\s+", " ", content)

    # 3️⃣ Menü ve link satırlarını sil
    lines = content.split(".")
    cleaned_lines = []

    for line in lines:
        if any(word in line for word in BLACKLIST):
            continue
        if len(line.strip()) < 5:   # çok kısa anlamsız satırları at
            continue
        cleaned_lines.append(line.strip())

    return ". ".join(cleaned_lines)


def process_all_files():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".txt"):
            input_path = os.path.join(INPUT_DIR, filename)

            with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            cleaned = clean_text(content)

            output_path = os.path.join(OUTPUT_DIR, filename)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            print(f"Temizlendi: {filename}")


if __name__ == "__main__":
    process_all_files()