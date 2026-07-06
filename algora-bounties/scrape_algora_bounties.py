#!/usr/bin/env python3
"""
Scrape bounties from Algora API for relevant orgs.
Uses public endpoints and saves to CSV.
"""
import csv
import json
import os
import re
import sys
from pathlib import Path
import requests

ORGS = ["formbricks", "twentyhq", "novuhq", "hoppscotch", "documenso"]
API_BASE = "https://algora.io/api/v1/bounties?org={org}"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
OUTPUT_DIR = Path(__file__).parent.resolve()
CSV_PATH = OUTPUT_DIR / "algora_bounties.csv"


def fetch_bounties(org: str) -> list[dict] | None:
    url = API_BASE.format(org=org)
    try:
        resp = requests.get(url, timeout=15, headers=HEADERS)
        resp.raise_for_status()
        # Algora returns HTML when rate limited or not found; try to extract JSON from HTML
        try:
            data = resp.json()
        except ValueError:
            # Try to find JSON in script tag (Algora uses SSR)
            json_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', resp.text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
            else:
                print(f"[!] Could not parse JSON for {org}: HTML response received", file=sys.stderr)
                return None
        return data
    except Exception as e:
        print(f"[!] Error fetching {org}: {e}", file=sys.stderr)
        return None


def extract_bounty_fields(bounty: dict) -> dict:
    repo_url = bounty.get("repo_url", bounty.get("repository", {}).get("html_url", ""))
    return {
        "org": bounty.get("org", bounty.get("organization", {}).get("login", "")),
        "repo": repo_url.split("/")[-2] if repo_url else "",
        "bounty_url": repo_url,
        "reward_usd": bounty.get("reward", bounty.get("amount", 0)),
        "status": bounty.get("status", bounty.get("state", "")),
    }


def main():
    rows = []
    for org in ORGS:
        print(f"[+] Fetching bounties for {org}...")
        bounties = fetch_bounties(org)
        if not bounties:
            continue
        if isinstance(bounties, list):
            for b in bounties:
                rows.append(extract_bounty_fields(b))
        elif isinstance(bounties, dict):
            # Single bounty object
            rows.append(extract_bounty_fields(bounties))

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