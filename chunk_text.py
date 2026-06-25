import os

INPUT_DIR = "data/clean_txt"
OUTPUT_DIR = "data/chunks"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

os.makedirs(OUTPUT_DIR, exist_ok=True)


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []

    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)

    return chunks


def process_all_files():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".txt"):
            input_path = os.path.join(INPUT_DIR, filename)

            with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

            chunks = chunk_text(text)

            base_name = os.path.splitext(filename)[0]

            for i, chunk in enumerate(chunks):
                output_filename = f"{base_name}_chunk_{i+1}.txt"
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(chunk)

            print(f"{filename} -> {len(chunks)} chunk oluşturuldu.")


if __name__ == "__main__":
    process_all_files()