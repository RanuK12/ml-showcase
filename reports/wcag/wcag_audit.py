#!/usr/bin/env python3
"""
WCAG Audit Tool — Ranuk IT Solutions
Ejecuta axe-core sobre una URL y genera reporte PDF con hallazgos.
Uso: python3 wcag_audit.py <url> [--output reporte.pdf]
"""

import sys
import os
import json
import subprocess
import tempfile
import argparse
from datetime import datetime

RANUKITA_REPORT = os.path.expanduser("~/Apps/ranukita-bridge/scripts/ranukita_report.py")
LOGO = os.path.expanduser("~/Apps/ranukita-bridge/assets/ranukita-logo.png")
REPORTS_DIR = os.path.expanduser("~/Desktop/Oficina_Ranuk/reports/wcag")

def _find_chrome_paths():
    """Auto-detecta Chrome for Testing y ChromeDriver del browser-driver-manager."""
    bdm = os.path.expanduser("~/.browser-driver-manager")
    chrome_dir = os.path.join(bdm, "chrome")
    cd_dir = os.path.join(bdm, "chromedriver")
    chrome_path = chromedriver_path = None
    if os.path.isdir(chrome_dir):
        vers = sorted([d for d in os.listdir(chrome_dir) if d.startswith("mac_arm-")], reverse=True)
        if vers:
            chrome_path = os.path.join(chrome_dir, vers[0],
                "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")
    if os.path.isdir(cd_dir):
        vers = sorted([d for d in os.listdir(cd_dir) if d.startswith("mac_arm-")], reverse=True)
        if vers:
            chromedriver_path = os.path.join(cd_dir, vers[0],
                "chromedriver-mac-arm64/chromedriver")
    return chrome_path, chromedriver_path

def run_axe(url: str) -> dict:
    """Ejecuta axe-core CLI sobre la URL y devuelve el JSON parseado."""
    cmd = ["axe", url, "--show-errors", "--exit", "-j", "--stdout"]
    chrome_path, cd_path = _find_chrome_paths()
    if chrome_path and os.path.isfile(chrome_path):
        cmd.extend(["--chrome-path", chrome_path])
    if cd_path and os.path.isfile(cd_path):
        cmd.extend(["--chromedriver-path", cd_path])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode not in (0, 1):  # axe devuelve 1 si encuentra violaciones
        print(f"⚠️  axe-core exit code: {result.returncode}")
    # Intentar stdout primero, si está vacío probar stderr (axe a veces saca JSON ahí)
    raw = result.stdout.strip()
    if not raw:
        raw = result.stderr.strip()
    try:
        data = json.loads(raw)
        # axe devuelve una lista con un solo dict
        if isinstance(data, list) and len(data) > 0:
            return data[0]
        return data
    except json.JSONDecodeError:
        print("❌ Error parseando salida de axe-core")
        print(f"stdout: {result.stdout[:300]}")
        print(f"stderr: {result.stderr[:300]}")
        sys.exit(1)

def classify_violations(data: dict) -> dict:
    """Clasifica violaciones por severidad."""
    violations = data.get("violations", [])
    classified = {"critical": [], "serious": [], "moderate": [], "minor": []}
    for v in violations:
        impact = v.get("impact", "minor")
        if impact in classified:
            classified[impact].append(v)
        else:
            classified["minor"].append(v)
    return classified

def build_report_spec(url: str, data: dict, classified: dict) -> dict:
    """Construye el spec JSON para ranukita_report.py."""
    violations = data.get("violations", [])
    passes = data.get("passes", [])
    inapplicable = data.get("inapplicable", [])
    
    url_clean = url.replace("https://", "").replace("http://", "").rstrip("/")
    
    sections = []
    
    # Resumen
    total_violations = len(violations)
    total_passes = len(passes)
    summary_bullets = [
        f"Violaciones encontradas: {total_violations}",
        f"Reglas pasadas: {total_passes}",
        f"Reglas no aplicables: {len(inapplicable)}",
    ]
    for impact, items in classified.items():
        if items:
            summary_bullets.append(f"  • {impact.title()}: {len(items)}")
    
    sections.append({
        "heading": "1. Resumen de Auditoría",
        "paragraphs": [
            f"Auditoría de accesibilidad WCAG realizada sobre {url} utilizando axe-core v4.11.",
            f"Se evaluaron {total_violations + total_passes} reglas WCAG 2.1 AA en total."
        ],
        "bullets": summary_bullets
    })
    
    # Violaciones por severidad
    severity_order = ["critical", "serious", "moderate", "minor"]
    for impact in severity_order:
        items = classified.get(impact, [])
        if not items:
            continue
        
        table_rows = []
        for v in items[:15]:  # top 15 por severidad
            desc = v.get("description", "")[:80]
            wcag = ", ".join(v.get("tags", []))[:60]
            nodes = len(v.get("nodes", []))
            table_rows.append([desc, wcag, str(nodes)])
        
        section = {
            "heading": f"2. Violaciones {impact.title()} ({len(items)})",
            "paragraphs": [f"Se encontraron {len(items)} violaciones de nivel {impact}."]
        }
        if table_rows:
            section["table"] = {
                "headers": ["Descripción", "Criterio WCAG", "Elementos"],
                "rows": table_rows
            }
        sections.append(section)
    
    # Reglas pasadas (top 10)
    if passes:
        pass_rows = []
        for p in passes[:10]:
            pass_rows.append([p.get("description", "")[:80], p.get("impact", "N/A")])
        sections.append({
            "heading": "3. Reglas Superadas (10 de {})".format(len(passes)),
            "table": {
                "headers": ["Descripción", "Impacto"],
                "rows": pass_rows
            }
        })
    
    # Recomendaciones
    rec_bullets = [
        "Corregir primero las violaciones CRITICAL: afectan usuarios con discapacidades severas.",
        "Las violaciones SERIOUS suelen implicar barreras significativas de navegación.",
        "Priorizar remediación por página de alto tráfico (homepage, checkout, login).",
        "Volver a auditar después de cada ronda de correcciones.",
        "Mantener un registro de accesibilidad como parte del pipeline de CI/CD."
    ]
    sections.append({
        "heading": "4. Recomendaciones",
        "bullets": rec_bullets
    })
    
    return {
        "title": f"Auditoría WCAG — {url_clean}",
        "subtitle": "Informe de Accesibilidad Web",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sections": sections
    }

def main():
    parser = argparse.ArgumentParser(description="WCAG Audit Tool — Ranuk IT Solutions")
    parser.add_argument("url", help="URL a auditar (ej: https://ejemplo.com)")
    parser.add_argument("--output", "-o", help="Ruta del PDF de salida")
    args = parser.parse_args()
    
    url = args.url
    if not url.startswith("http"):
        url = "https://" + url
    
    # Output path
    if args.output:
        output_path = args.output
    else:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").rstrip("_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(REPORTS_DIR, f"wcag_{safe_name}_{timestamp}.pdf")
    
    print(f"🔍 Analizando {url} con axe-core...")
    data = run_axe(url)
    
    classified = classify_violations(data)
    spec = build_report_spec(url, data, classified)
    
    # Guardar spec temporal
    spec_path = output_path.replace(".pdf", "_spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Generando reporte PDF...")
    result = subprocess.run(
        ["python3", RANUKITA_REPORT, spec_path, output_path, "--theme", "dark"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Error generando PDF: {result.stderr}")
        sys.exit(1)
    
    print(f"✅ Reporte generado: {output_path}")
    print(f"   Spec JSON: {spec_path}")
    
    # Limpiar spec temporal
    os.remove(spec_path)

if __name__ == "__main__":
    main()
