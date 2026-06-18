set -euo pipefail
CHECKPOINT=~/.ranukita/checkpoints/4fbd9f.md
mkdir -p "$(dirname "$CHECKPOINT")"
echo "## $(date) – inicio del proceso masivo" > "$CHECKPOINT"
for repo_path in ~/Desktop/Oficina_Ranuk/*; do
  if [ -d "$repo_path/.git" ]; then
    repo_name=$(basename "$repo_path")
    echo ">> Procesando $repo_name"
    cd "$repo_path"
    git checkout -B ranukita/4fbd9f || { echo "- $repo_name – error al crear branch" >> "$CHECKPOINT"; continue; }
    if [ ! -f README.md ]; then
      echo "# $repo_name" > README.md
      echo "Descripción breve del proyecto $repo_name." >> README.md
      git add README.md
      git commit -m "add README [ranukita:4fbd9f]" || true
      echo "- $repo_name – README creado" >> "$CHECKPOINT"
    fi
    if [ -n "$(git status -s)" ]; then
      git add -A
      git commit -m "commit pending changes [ranukita:4fbd9f]" || true
      echo "- $repo_name – cambios commiteados" >> "$CHECKPOINT"
    fi
    remote_url="https://github.com/RanuK12/${repo_name}.git"
    git remote remove origin || true
    git remote add origin "$remote_url" || true
    if git push -u origin ranukita/4fbd9f; then
      echo "- $repo_name – push OK" >> "$CHECKPOINT"
    else
      echo "- $repo_name – push FAILED (repo puede estar archivado o sin permisos)" >> "$CHECKPOINT"
    fi
  fi
done
echo "## $(date) – proceso masivo finalizado" >> "$CHECKPOINT"
