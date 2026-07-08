#!/usr/bin/env python3
# auto_youtube_downloader.py — Descarga videos de YouTube a alta calidad usando yt-dlp.
# Requiere: yt-dlp instalado (pip install yt-dlp).

import subprocess
from pathlib import Path

def descargar_video_youtube(url, output_dir=Path.home() / "Downloads" / "YouTube"):
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "-o", str(output_dir / "%(title)s.%(ext)s"),
            url
        ]
        subprocess.run(cmd, check=True)
        print("✅ Video descargado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al descargar: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python3 auto_youtube_downloader.py <URL de YouTube>")
    else:
        descargar_video_youtube(sys.argv[1])