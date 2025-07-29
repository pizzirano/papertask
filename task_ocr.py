import sqlite3
import sys
import os
import pytesseract
from PIL import Image
import pillow_heif
DB_PATH = "tarefas.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            status TEXT DEFAULT 'pendente'
        )
    """)
    conn.commit()
    conn.close()

def process_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="por")  # OCR em português
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO tarefas (filename, conteudo) VALUES (?, ?)", 
                    (os.path.basename(image_path), text.strip()))
        conn.commit()
        conn.close()
        print(f"[OK] OCR finalizado e salvo no banco: {image_path}")
    except Exception as e:
        print(f"[ERRO] Falha ao processar {image_path}: {e}")

if __name__ == "__main__":
    init_db()
    if len(sys.argv) > 1:
        process_image(sys.argv[1])
    else:
        print("Uso: python task_ocr.py <caminho_da_imagem>")
