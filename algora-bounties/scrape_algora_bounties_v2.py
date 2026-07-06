#!/usr/bin/env python3
"""
Scrape bounties from Algora public listing.
Uses public /bounties page and extracts bounty cards.
"""
import csv
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = Path(__file__).parent.resolve()
CSV_PATH = OUTPUT_DIR / "algora_bounties_v2.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}


def fetch_bounties_page() -> str | None:
    url = "https://algora.io/bounties"
    try:
        resp = requests.get(url, timeout=15, headers=HEADERS)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[!] Failed to fetch Algora bounties page: {e}", file=sys.stderr)
        return None


def parse_bounties(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("div.max-w-md, div.w-full, article, [data-testid='bounty-card']"):
        org_el = card.select_one("a[href*='/orgs/']")
        bounty_el = card.select_one("a[href*='/bounties/']")
        reward_el = card.select_one("div.font-bold, span.text-lg.font-semibold")
        status_el = card.select_one("span.bg-green-100, span.bg-blue-100, span.px-2.py-1.rounded-full.text-xs")

        org = org_el.text.strip() if org_el else ""
        bounty_url = bounty_el.get("href", "") if bounty_el else ""
        if not bounty_url.startswith("http"):
            bounty_url = f"https://algora.io{bounty_url}" if bounty_url else ""
        reward_text = reward_el.text.strip() if reward_el else "0"
        reward_usd = _parse_reward(reward_text)
        status = status_el.text.strip() if status_el else ""

        rows.append({
            "org": org,
            "repo": "",
            "bounty_url": bounty_url,
            "reward_usd": reward_usd,
            "status": status,
        })
    return rows


def _parse_reward(text: str) -> int:
    text = text.lower().replace("$", "").replace(",", "").strip()
    m = re.search(r"\d+\.?\d*", text)
    return int(float(m.group(0))) if m else 0


def main():
    html = fetch_bounties_page()
    if not html:
        return 1

    bounties = parse_bounties(html)
    if not bounties:
        print("[!] No bounties found on page.")
        return 1

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["org", "repo", "bounty_url", "reward_usd", "status"]
        )
        writer.writeheader()
        writer.writerows(bounties)

    print(f"[✓] Saved {len(bounties)} bounties to {CSV_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
