#!/usr/bin/env python3
"""
Scrape bounties from Algora bounties page for relevant orgs.
Uses web scraping since Algora does not provide a public API for bounties per org.

The public page at https://algora.io/bounties lists all available bounties.
We filter by the specified orgs and save to CSV.
"""
import csv
import os
import re
import sys
from pathlib import Path
import requests

# Target orgs (Python/TypeScript, $100-500)
ORGS = ["formbricks", "twentyhq", "novuhq", "hoppscotch", "documenso"]
OUTPUT_DIR = Path(__file__).parent.resolve()
CSV_PATH = OUTPUT_DIR / "algora_bounties.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}


def fetch_bounties_page() -> str | None:
    try:
        resp = requests.get("https://algora.io/bounties", timeout=20, headers=HEADERS)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[!] Error fetching Algora bounties page: {e}", file=sys.stderr)
        return None


def scrape_bounties(text: str) -> list[dict]:
    bounties = []
    # Look for bounty cards on the page
    pattern = re.compile(r'<div[^>]*class="[^"]*bounty[^"]*"[^>]*>.*?<a\s+href="(/bounties/[^"]+)"[^>]*>(.*?)</a>.*?class="[^"]*org[^"]*">\s*([^<]+)\s*</span>.*?class="[^"]*reward[^"]*">\s*([\$\d,]+)\s*</span>', re.DOTALL | re.IGNORECASE)
    seen = set()
    for link, title, org, reward in pattern.findall(text):
        org = org.strip()
        if org in ORGS and org not in seen:
            seen.add(org)
            bounties.append({
                "org": org,
                "repo": "",  # We don't have repo from this scrape; leave empty
                "bounty_url": f"https://algora.io{link}",
                "reward_usd": int(reward.replace(",", "").replace("$", "")),
                "status": "open"
            })
    return bounties


def main() -> int:
    page = fetch_bounties_page()
    if not page:
        print("[!] Failed to fetch bounties page. Exiting.")
        return 1

    bounties = scrape_bounties(page)
    if not bounties:
        print("[!] No bounties found for target orgs. Exiting.")
        return 1

    with CSV_PATH.open("w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["org", "repo", "bounty_url", "reward_usd", "status"])
        writer.writeheader()
        writer.writerows(bounties)

    print(f"[✓] Saved {len(bounties)} bounties to {CSV_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
