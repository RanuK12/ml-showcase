#!/usr/bin/env python3
# automate_github_backup.py — Backup automático de repositorios GitHub locales a un directorio de backup.
# Requiere: tener git instalado y acceso a los repositorios locales.

import os
import shutil
from pathlib import Path

def backup_github_repos(origen=Path.home() / "GitHub", destino=Path.home() / "GitHub_Backup"):
    if not origen.exists():
        print("❌ El directorio ~/GitHub no existe.")
        return

    destino.mkdir(exist_ok=True)

    repos_backeados = 0
    for repo_dir in origen.iterdir():
        if repo_dir.is_dir() and (repo_dir / ".git").exists():
            destino_repo = destino / repo_dir.name
            shutil.copytree(repo_dir, destino_repo, dirs_exist_ok=True)
            print(f"✅ Backup de {repo_dir.name} → {destino_repo}")
            repos_backeados += 1

    print(f"\n📂 Backup completado. Repositorios respaldados: {repos_backeados}")

if __name__ == "__main__":
    backup_github_repos()