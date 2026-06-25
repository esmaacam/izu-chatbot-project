import os
import subprocess

PDF_DIR = "data/pdf"
OUTPUT_DIR = "data/pdf_txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_pdf(pdf_path, output_path):
    subprocess.run([
        "pdftotext",
        "-layout",
        pdf_path,
        output_path
    ])

def process_all():
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, file)
            output_file = file.replace(".pdf", ".txt")
            output_path = os.path.join(OUTPUT_DIR, output_file)

            convert_pdf(pdf_path, output_path)
            print("Dönüştürüldü:", file)

if __name__ == "__main__":
    process_all()