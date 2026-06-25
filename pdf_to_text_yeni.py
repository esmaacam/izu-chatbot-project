import pdfplumber
import os

# PDF dosyalarının olduğu klasör
PDF_DIR = "data/pdf"
# Çıktıların olacağı klasör
OUTPUT_DIR = "data/clean_txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def pdf_metne_cevir():
    for dosya_adi in os.listdir(PDF_DIR):
        if dosya_adi.endswith(".pdf"):
            pdf_yolu = os.path.join(PDF_DIR, dosya_adi)
            txt_yolu = os.path.join(OUTPUT_DIR, dosya_adi.replace(".pdf", ".txt"))
            
            with pdfplumber.open(pdf_yolu) as pdf:
                tum_metin = ""
                for sayfa in pdf.pages:
                    metin = sayfa.extract_text()
                    if metin:
                        tum_metin += metin + "\n"
                
            with open(txt_yolu, "w", encoding="utf-8") as f:
                f.write(tum_metin)
            
            print(f"Dönüştürüldü: {dosya_adi}")

if __name__ == "__main__":
    pdf_metne_cevir()