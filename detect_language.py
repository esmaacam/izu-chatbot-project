from pathlib import Path
from langdetect import detect

INPUT_DIR = Path("data/chunks")
TR_DIR = Path("data/chunks_tr")
EN_DIR = Path("data/chunks_en")

TR_DIR.mkdir(parents=True, exist_ok=True)
EN_DIR.mkdir(parents=True, exist_ok=True)

for chunk in INPUT_DIR.glob("*.txt"):
    text = chunk.read_text(encoding="utf-8", errors="ignore")

    try:
        lang = detect(text)
    except:
        continue

    if lang == "tr":
        chunk.rename(TR_DIR / chunk.name)
    elif lang == "en":
        chunk.rename(EN_DIR / chunk.name)

print("Dil ayrımı tamamlandı.")
