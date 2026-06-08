#!/bin/bash
# ============================================================
# build.sh — Empaqueta el starter kit en un solo archivo .com
# Uso: ./build.sh [nombre-del-archivo]
# Requiere: redbean.com (o redbean-demo.com) y zip
# ============================================================

set -e

OUT="${1:-my-landing.com}"
REDBEAN_URL="https://redbean.dev/redbean-latest.com"

echo "📦 Building landing page package..."

# Descargar redbean si no existe
if [ ! -f "redbean.com" ]; then
    echo "⬇️  Descargando redbean..."
    curl -sL "$REDBEAN_URL" -o redbean.com
    chmod +x redbean.com
fi

# Crear paquete temporal
TMPDIR=$(mktemp -d)
cp redbean.com "$TMPDIR/$OUT"
cp index.html style.css "$TMPDIR/"

# Copiar landing.lua como /.init.lua (Redbean lo busca en la raíz del ZIP)
cp landing.lua "$TMPDIR/.init.lua"

cd "$TMPDIR"

# Empaquetar archivos en el .com
# .init.lua DEBE estar en la raíz del ZIP (ruta /.init.lua)
zip -j "$OUT" index.html style.css .init.lua

cd - > /dev/null
cp "$TMPDIR/$OUT" .
rm -rf "$TMPDIR"

chmod +x "$OUT"
echo ""
echo "✅ Listo: ./$OUT"
echo "   Ejecutalo con: ./$OUT"
echo "   Landing: http://localhost:8080"
echo "   Leads:   http://localhost:8080/leads"
echo ""
echo "📏 Tamaño: $(ls -lh "$OUT" | awk '{print $5}')"
