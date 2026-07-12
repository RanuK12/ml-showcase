#!/usr/bin/env python3
"""
[ranukita:971332] Script diario para escanear bounties en plataformas.
Filtra bounties relevantes con pago confirmado y genera informe PDF.
"""
import csv
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from fpdf import FPDF

# Configuración
ORGS = ["formbricks", "twentyhq", "novuhq", "hoppscotch", "documenso"]
BOUNTIES_DIR = Path.home() / "Desktop" / "Oficina_Ranuk" / "bounties"
CSV_PATH = BOUNTIES_DIR / "algora_bounties.csv"
PDF_PATH = BOUNTIES_DIR / f"bounties_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}


def fetch_bounties_page() -> str | None:
    """Fetch bounties page from Algora."""
    try:
        resp = requests.get("https://algora.io/bounties", timeout=20, headers=HEADERS)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[!] Error fetching Algora bounties page: {e}", file=sys.stderr)
        return None


def parse_bounties(html: str) -> list[dict]:
    """Parse bounties from HTML, filtering by target orgs and confirmed payment."""
    bounties = []
    pattern = re.compile(
        r'<div[^>]*class="[^"]*bounty[^"]*"[^>]*>.*?<a\s+href="(/bounties/[^"]+)"[^>]*>(.*?)</a>.*?class="[^"]*org[^"]*">\s*([^<]+)\s*</span>.*?class="[^"]*reward[^"]*">\s*([\$\d,]+)\s*</span>',
        re.DOTALL | re.IGNORECASE
    )
    seen = set()
    for link, title, org, reward in pattern.findall(html):
        org = org.strip()
        if org in ORGS and org not in seen:
            seen.add(org)
            reward_usd = _parse_reward(reward)
            if reward_usd >= 100:
                bounties.append({
                    "org": org,
                    "repo": "",
                    "bounty_url": f"https://algora.io{link}",
                    "reward_usd": reward_usd,
                    "status": "open"
                })
    return bounties


def _parse_reward(text: str) -> int:
    """Extract numeric reward from text like '$500'."""
    match = re.search(r'[\d,]+', text.replace(",", ""))
    return int(match.group()) if match else 0


def save_to_csv(bounties: list[dict]) -> None:
    """Save bounties to CSV file."""
    BOUNTIES_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["org", "repo", "bounty_url", "reward_usd", "status"])
        writer.writeheader()
        writer.writerows(bounties)
    print(f"[✓] CSV guardado en: {CSV_PATH}")


def generate_pdf_report(bounties: list[dict]) -> None:
    """Generate PDF report with bounty details and URLs."""
    BOUNTIES_DIR.mkdir(parents=True, exist_ok=True)

    class BountiesPDF(FPDF):
        def header(self):
            self.set_fill_color(26, 95, 57)
            self.rect(0, 0, 210, 25, 'F')
            self.set_font("Helvetica", "B", 18)
            self.set_text_color(255, 255, 255)
            self.set_y(5)
            self.cell(0, 15, "Informe de Bounties", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(0, 0, 0)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    pdf = BountiesPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Fecha
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Resumen
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Total de bounties encontrados: {len(bounties)}", new_x="LMARGIN", new_y="NEXT")
    total_reward = sum(b["reward_usd"] for b in bounties)
    pdf.cell(0, 10, f"Recompensa total: ${total_reward:,}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Tabla de bounties
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(200, 200, 200)
    col_widths = [40, 50, 30, 70]
    headers = ["Organización", "Recompensa", "Estado", "URL"]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for bounty in bounties:
        pdf.cell(col_widths[0], 10, bounty["org"][:15], border=1)
        pdf.cell(col_widths[1], 10, f"${bounty['reward_usd']:,}", border=1)
        pdf.cell(col_widths[2], 10, bounty["status"], border=1)
        pdf.cell(col_widths[3], 10, bounty["bounty_url"][:30] + "...", border=1)
        pdf.ln()

    pdf.output(str(PDF_PATH))
    print(f"[✓] PDF generado en: {PDF_PATH}")


def main() -> int:
    """Main function to scan and generate report."""
    print("[*] Iniciando escaneo de bounties...")

    page = fetch_bounties_page()
    if not page:
        print("[!] No se pudo obtener la página de bounties.")
        return 1

    bounties = parse_bounties(page)
    if not bounties:
        print("[!] No se encontraron bounties para las organizaciones objetivo.")
        return 1

    save_to_csv(bounties)
    generate_pdf_report(bounties)

    print(f"\n[✓] Proceso completado. {len(bounties)} bounties encontrados.")
    print(f"    CSV: {CSV_PATH}")
    print(f"    PDF: {PDF_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
