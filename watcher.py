import os
import time
import sqlite3
from PIL import Image
import pillow_heif
import pytesseract

WATCH_FOLDER = "input"
DB_FILE = "tarefas.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def process_image(file_path):
    try:
        print(f"📌 Processando: {file_path}")

        # Detecta HEIC e converte para JPG
        if file_path.lower().endswith(".heic"):
            heif_file = pillow_heif.read_heif(file_path)
            img = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw"
            )
            new_path = file_path.rsplit(".", 1)[0] + ".jpg"
            img.save(new_path, "JPEG")
            file_path = new_path
            print(f"✅ Convertido HEIC → JPG: {new_path}")

        # Executa OCR
        text = pytesseract.image_to_string(Image.open(file_path), lang="por")
        if text.strip():
            save_task(text.strip())
            print(f"✅ OCR extraído e salvo: {text.strip()[:50]}...")
        else:
            print("⚠️ Nenhum texto reconhecido.")

    except Exception as e:
        print(f"[ERRO] Falha em {file_path}: {e}")

def save_task(text):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO tarefas (titulo) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def watch_folder():
    print(f"👀 Observando a pasta: {WATCH_FOLDER}")
    processed = set()
    while True:
        for filename in os.listdir(WATCH_FOLDER):
            path = os.path.join(WATCH_FOLDER, filename)
            if path not in processed and os.path.isfile(path):
                process_image(path)
                processed.add(path)
        time.sleep(5)

if __name__ == "__main__":
    init_db()
    watch_folder()
