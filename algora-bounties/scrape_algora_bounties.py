#!/usr/bin/env python3
"""
Scrape bounties from Algora API for relevant orgs.
Uses public endpoints and saves to CSV.
"""
import csv
import json
import os
import sys
from pathlib import Path
import requests

ORGS = ["formbricks", "twentyhq", "novuhq", "documenso"]
API_BASE = "https://algora.io/api/bounties?org={org}"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
OUTPUT_DIR = Path(__file__).parent.resolve()
CSV_PATH = OUTPUT_DIR / "algora_bounties.csv"


def fetch_bounties(org: str) -> list[dict] | None:
    url = API_BASE.format(org=org)
    try:
        resp = requests.get(url, timeout=10, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.JSONDecodeError as e:
        print(f"[!] JSONDecodeError fetching {org}: {e} | response text len={len(resp.text)} | snippet={resp.text[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[!] Error fetching {org}: {e}", file=sys.stderr)
        return None


def extract_bounty_fields(bounty: dict) -> dict:
    repo_url = bounty.get("repo_url", "")
    return {
        "org": bounty.get("org", ""),
        "repo": repo_url.split("/")[-2] if repo_url else "",
        "bounty_url": repo_url,
        "reward_usd": bounty.get("reward", 0),
        "status": bounty.get("status", ""),
    }


def main():
    rows = []
    for org in ORGS:
        print(f"[+] Fetching bounties for {org}...")
        bounties = fetch_bounties(org)
        if not bounties:
            continue
        for b in bounties:
            rows.append(extract_bounty_fields(b))

    if not rows:
        print("[!] No bounties fetched. Exiting.")
        return 1

    with CSV_PATH.open("w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["org", "repo", "bounty_url", "reward_usd", "status"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] Saved {len(rows)} bounties to {CSV_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
