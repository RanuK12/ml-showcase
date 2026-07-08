#!/usr/bin/env python3
# clean_downloads_folder.py — Organiza archivos del directorio ~/Downloads por tipo y fecha
# Uso: python3 clean_downloads_folder.py

import os
import shutil
from datetime import datetime
from pathlib import Path

def organizar_descargas():
    downloads = Path.home() / "Downloads"
    if not downloads.exists():
        print("❌ El directorio ~/Downloads no existe.")
        return

    categorias = {
        "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
        "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
        "Música": [".mp3", ".wav", ".flac", ".aac"],
        "Archivos": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Ejecutables": [".exe", ".msi", ".dmg"],
        "Código": [".py", ".js", ".html", ".css", ".json", ".md", ".sh"],
    }

    # Crear subdirectorios si no existen
    for categoria in categorias:
        (downloads / categoria).mkdir(exist_ok=True)

    # Mover archivos
    movidos = 0
    for archivo in downloads.iterdir():
        if archivo.is_file():
            ext = archivo.suffix.lower()
            destino = None
            for categoria, extensiones in categorias.items():
                if ext in extensiones:
                    destino = downloads / categoria / archivo.name
                    if destino.exists():
                        # Si existe, añadir timestamp para evitar colisión
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        destino = downloads / categoria / f"{archivo.stem}_{timestamp}{ext}"
                    shutil.move(str(archivo), str(destino))
                    movidos += 1
                    print(f"✅ {archivo.name} → {categoria}/")
                    break
            if destino is None:
                # Archivos sin categoría conocida van a "Otros"
                otros = downloads / "Otros"
                otros.mkdir(exist_ok=True)
                destino = otros / archivo.name
                if destino.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    destino = otros / f"{archivo.stem}_{timestamp}{ext}"
                shutil.move(str(archivo), str(destino))
                movidos += 1
                print(f"✅ {archivo.name} → Otros/")

    print(f"\n📂 Proceso completado. Archivos movidos: {movidos}")

if __name__ == "__main__":
    organizar_descargas()