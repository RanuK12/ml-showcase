#!/usr/bin/env python3
"""
ADA Audits — Pipeline automatizado de generación PDF + Gumroad.
[ranukita:b4f1fb]

Flujo:
  1. Toma un spec JSON de entrada (datos de auditoría)
  2. Genera PDF profesional con ranukita_report.py
  3. Opcional: genera enlace de compra único por cliente (vía Gumroad License API)
  4. Opcional: sube el PDF como asset del producto en Gumroad

Uso:
  python3 ada_pipeline.py <input_spec.json> [--output reporte.pdf] [--link cliente@email.com] [--upload]

Ejemplos:
  # Generar PDF
  python3 ada_pipeline.py example_spec.json --output reporte.pdf

  # Generar PDF + enlace único para un cliente
  python3 ada_pipeline.py spec.json --output reporte.pdf --link cliente@empresa.com

  # Generar PDF + enlace + subir a Gumroad
  python3 ada_pipeline.py spec.json --output reporte.pdf --link cliente@empresa.com --upload
"""

import sys
import os
import json
import subprocess
import datetime

RANUKITA_REPORT = os.path.expanduser("~/Apps/ranukita-bridge/scripts/ranukita_report.py")
GUMROAD_CONFIG = os.path.join(os.path.dirname(__file__), "gumroad_config.json")
CONTENT_MD = os.path.join(os.path.dirname(__file__), "content.md")

# ── helpers ──────────────────────────────────────────────────────────────

def load_spec(path):
    with open(path) as f:
        return json.load(f)

def build_report_spec(audit_data):
    """Convierte datos de auditoría en el spec JSON de ranukita_report.py."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    sections = []

    # Sección 1: Resumen
    resumen = audit_data.get("resumen", {})
    s1 = {
        "heading": "1. Resumen Ejecutivo",
        "paragraphs": [resumen.get("texto", "Sin datos de resumen.")],
        "bullets": resumen.get("puntos", []),
    }
    sections.append(s1)

    # Sección 2: Hallazgos
    hallazgos = audit_data.get("hallazgos", [])
    if hallazgos:
        s2 = {
            "heading": "2. Hallazgos Detectados",
            "table": {
                "headers": ["ID", "Severidad", "Descripción", "Estado"],
                "rows": [
                    [h.get("id",""), h.get("severidad",""), h.get("descripcion",""), h.get("estado","")]
                    for h in hallazgos
                ],
            },
        }
        sections.append(s2)

    # Sección 3: Recomendaciones
    recs = audit_data.get("recomendaciones", [])
    if recs:
        s3 = {
            "heading": "3. Recomendaciones",
            "bullets": recs,
        }
        sections.append(s3)

    # Sección 4: Métricas
    metrics = audit_data.get("metricas", {})
    if metrics:
        s4 = {
            "heading": "4. Métricas Clave",
            "table": {
                "headers": ["Métrica", "Valor", "Benchmark", "Estado"],
                "rows": [
                    [m["nombre"], m["valor"], m.get("benchmark",""), m.get("estado","")]
                    for m in metrics
                ],
            },
        }
        sections.append(s4)

    return {
        "title": f"ADA Audit — {audit_data.get('cliente', 'Cliente')}",
        "subtitle": f"Auditoría de Datos | Generado: {now}",
        "date": datetime.date.today().isoformat(),
        "sections": sections,
    }

def generate_pdf(spec, output_path):
    """Ejecuta ranukita_report.py con el spec."""
    spec_path = output_path.replace(".pdf", "_spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)

    cmd = [sys.executable, RANUKITA_REPORT, spec_path, output_path, "--theme", "dark"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error generando PDF: {result.stderr}")
        return False
    print(f"✅ PDF generado: {output_path}")
    return True

def generate_unique_link(cliente_email, token):
    """Genera un enlace de compra único por cliente usando Gumroad License API.
    
    Crea una licencia vinculada al email del cliente que permite:
    - Acceso directo al producto sin pasar por checkout público
    - Seguimiento individual por cliente
    - Posibilidad de revocar acceso si es necesario
    
    Args:
        cliente_email: Email del cliente para asociar la licencia
        token: Gumroad access token
        
    Returns:
        str: URL de compra única, o None si falló
    """
    import requests
    config = json.load(open(GUMROAD_CONFIG))
    product_id = config.get("product_id")
    if not product_id:
        print("⚠️  No hay product_id en gumroad_config.json")
        return None
    
    url = f"https://api.gumroad.com/v2/licenses"
    data = {
        "access_token": token,
        "product_id": product_id,
        "email": cliente_email,
        "quantity": 1,
    }
    try:
        resp = requests.post(url, data=data)
        if resp.status_code in (200, 201):
            result = resp.json()
            license_key = result.get("license", {}).get("key", "")
            purchase_url = result.get("purchase_url", "")
            if purchase_url:
                print(f"✅ Enlace único generado para {cliente_email}: {purchase_url}")
                return purchase_url
            # Fallback: construir URL con license key
            base_url = config.get("gumroad_url", "https://tanquerade.gumroad.com/l/fnvgas")
            print(f"✅ Licencia generada para {cliente_email}: {license_key}")
            return f"{base_url}?license={license_key}"
        else:
            print(f"⚠️  Error generando licencia: {resp.status_code} {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"⚠️  Error en generate_unique_link: {e}")
        return None

def get_gumroad_token():
    """Lee token de Gumroad del .env del bridge."""
    env_path = os.path.expanduser("~/Apps/ranukita-bridge/.env")
    if not os.path.exists(env_path):
        print("⚠️  No se encontró .env del bridge. Gumroad upload requiere token.")
        return None
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("GUMROAD_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

def upload_to_gumroad(pdf_path, product_id, token):
    """Sube el PDF como asset de producto en Gumroad (API v2)."""
    import requests
    url = f"https://api.gumroad.com/v2/products/{product_id}/assets"
    with open(pdf_path, "rb") as f:
        files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
        data = {"access_token": token}
        resp = requests.post(url, data=data, files=files)
    if resp.status_code in (200, 201):
        print("✅ PDF subido a Gumroad como asset del producto.")
        return True
    else:
        print(f"⚠️  Error subiendo a Gumroad: {resp.status_code} {resp.text[:200]}")
        return False

# ── main ─────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 ada_pipeline.py <input_spec.json> [--output reporte.pdf] [--upload]")
        sys.exit(1)

    input_spec = sys.argv[1]
    output_path = None
    do_upload = False
    do_link = False
    cliente_email = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--output" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 1
        elif arg == "--upload":
            do_upload = True
        elif arg == "--link":
            do_link = True
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                cliente_email = sys.argv[i + 1]
                i += 1
        i += 1

    if not output_path:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"ada_audit_{ts}.pdf"

    # 1. Cargar datos de auditoría
    audit_data = load_spec(input_spec)

    # 2. Construir spec del reporte
    report_spec = build_report_spec(audit_data)

    # 3. Generar PDF
    ok = generate_pdf(report_spec, output_path)
    if not ok:
        sys.exit(1)

    # 4. Obtener token si vamos a interactuar con Gumroad
    token = None
    if do_upload or do_link:
        token = get_gumroad_token()
        if not token:
            print("⚠️  No hay GUMROAD_TOKEN en .env — omitiendo operaciones Gumroad")
            do_upload = False
            do_link = False

    # 5. Generar enlace único por cliente
    link_url = None
    if do_link:
        if not cliente_email:
            # Intentar sacar email del spec
            cliente_email = audit_data.get("cliente_email") or audit_data.get("email")
        if cliente_email:
            link_url = generate_unique_link(cliente_email, token)
        else:
            print("⚠️  --link requiere email del cliente. Pasalo como argumento o incluí 'cliente_email' en el spec JSON.")

    # 6. Upload opcional a Gumroad
    if do_upload:
        config = json.load(open(GUMROAD_CONFIG))
        pid = config.get("product_id")
        if pid:
            upload_to_gumroad(output_path, pid, token)
        else:
            print("⚠️  No hay product_id en gumroad_config.json")

    print(f"\n✅ Pipeline completo. Reporte: {output_path}")
    if link_url:
        print(f"🔗 Enlace de compra único: {link_url}")

if __name__ == "__main__":
    main()
