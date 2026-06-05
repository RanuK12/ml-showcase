#!/usr/bin/env python3
# (c) 2026 Ranuk IT Solutions
"""Freelance Gig Scraper via Camofox stealth browser."""
import json, os, re, sys, time, urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from pathlib import Path

CAMOFOX = "http://127.0.0.1:9377"
OUT = Path(__file__).resolve().parent
MIN_BUDGET = 200
QUERIES = ["automation bot", "scraping tool", "data pipeline", "API integration", "Python automation"]

def camo_ok():
    try:
        urllib.request.urlopen(f"{CAMOFOX}/health", timeout=5)
        return True
    except Exception:
        return False

def browse(url, retries=2):
    body = json.dumps({"url": url, "userId": "ranukita", "sessionKey": "ranukita"}).encode()
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(f"{CAMOFOX}/browse", data=body, method="POST",
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read())
                return d.get("content", d.get("html", ""))
        except Exception as e:
            if i < retries:
                time.sleep(3)
            else:
                print(f"  X Camofox error: {e}")
    return None

def parse_budget(txt):
    txt = txt.replace(",", "").replace("$", "")
    m = re.search(r"(\d+)\s*-\s*(\d+)", txt)
    if m: return float(m.group(1)), float(m.group(2))
    m = re.search(r"(\d+)", txt)
    if m: v = float(m.group(1)); return v, v
    return 0.0, 0.0


def scrape_upwork(q):
    gigs = []
    enc = q.replace(" ", "+")
    url = f"https://www.upwork.com/search/jobs/?q={enc}&sort=recency&budget=200-&posted=1"
    print(f"  -> Upwork: {q}")
    html = browse(url)
    if not html: return gigs
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("section.air3-card, [data-test='job-tile-list'] > div")
    if not cards: cards = soup.select("article, .job-tile")
    for c in cards[:20]:
        a = c.select_one("a[data-test='job-tile-title-link'], h2 a")
        title = a.get_text(strip=True) if a else ""
        href = a.get("href", "") if a else ""
        if href and not href.startswith("http"): href = "https://www.upwork.com" + href
        if not title: continue
        b = c.select_one("[data-test='budget'], .budget")
        bt = b.get_text(strip=True) if b else ""
        mn, mx = parse_budget(bt)
        if 0 < mx < MIN_BUDGET: continue
        d = c.select_one("[data-test='job-description-text']")
        dtxt = d.get_text(strip=True)[:500] if d else ""
        gigs.append(dict(title=title, platform="upwork", budget=bt or "Not specified",
                         budget_min=mn, budget_max=mx, description=dtxt, requirements="",
                         deadline="", posted_date="", url=href, query=q))
    return gigs

def scrape_freelancer(q):
    gigs = []
    enc = q.replace(" ", "%20")
    url = f"https://www.freelancer.com/jobs/?keyword={enc}&budget_min=200&time_submitted=1"
    print(f"  -> Freelancer: {q}")
    html = browse(url)
    if not html: return gigs
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.JobSearchCard-item, .project-list-item")
    for c in cards[:20]:
        a = c.select_one("a.JobSearchCard-primary-heading-link, h3 a")
        title = a.get_text(strip=True) if a else ""
        href = a.get("href", "") if a else ""
        if href and not href.startswith("http"): href = "https://www.freelancer.com" + href
        if not title: continue
        b = c.select_one(".JobSearchCard-secondary-price")
        bt = b.get_text(strip=True) if b else ""
        mn, mx = parse_budget(bt)
        if 0 < mx < MIN_BUDGET: continue
        gigs.append(dict(title=title, platform="freelancer", budget=bt or "Not specified",
                         budget_min=mn, budget_max=mx, description="", requirements="",
                         deadline="", posted_date="", url=href, query=q))
    return gigs

def scrape_fiverr(q):
    gigs = []
    enc = q.replace(" ", "+")
    url = f"https://www.fiverr.com/search/gigs?query={enc}&source=top-bar"
    print(f"  -> Fiverr: {q}")
    html = browse(url)
    if not html: return gigs
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("[data-testid='gig-card-layout'], .gig-card, [class*='search-result']")
    for c in cards[:20]:
        a = c.select_one("a[href*='gig']")
        title = a.get_text(strip=True) if a else ""
        href = a.get("href", "") if a else ""
        if href and not href.startswith("http"): href = "https://www.fiverr.com" + href
        if not title:
            h = c.select_one("h3, [class*='title']")
            title = h.get_text(strip=True) if h else ""
        if not title: continue
        b = c.select_one("[class*='price']")
        bt = b.get_text(strip=True) if b else ""
        mn, mx = parse_budget(bt)
        if 0 < mx < MIN_BUDGET: continue
        gigs.append(dict(title=title, platform="fiverr", budget=bt or "Not specified",
                         budget_min=mn, budget_max=mx, description="", requirements="",
                         deadline="", posted_date="", url=href, query=q))
    return gigs

def scrape_contra(q):
    gigs = []
    enc = q.replace(" ", "+")
    url = f"https://www.contra.com/opportunities?q={enc}"
    print(f"  -> Contra: {q}")
    html = browse(url)
    if not html: return gigs
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("[class*='opportunity'], [class*='listing'], article")
    for c in cards[:20]:
        a = c.select_one("a[href*='/opportunities/']")
        title = a.get_text(strip=True) if a else ""
        href = a.get("href", "") if a else ""
        if href and not href.startswith("http"): href = "https://www.contra.com" + href
        if not title:
            h = c.select_one("h2, h3")
            title = h.get_text(strip=True) if h else ""
        if not title: continue
        b = c.select_one("[class*='budget'], [class*='price']")
        bt = b.get_text(strip=True) if b else ""
        mn, mx = parse_budget(bt)
        if 0 < mx < MIN_BUDGET: continue
        gigs.append(dict(title=title, platform="contra", budget=bt or "Not specified",
                         budget_min=mn, budget_max=mx, description="", requirements="",
                         deadline="", posted_date="", url=href, query=q))
    return gigs

PLATFORMS = {"upwork": scrape_upwork, "freelancer": scrape_freelancer,
             "fiverr": scrape_fiverr, "contra": scrape_contra}

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Freelance gig scraper")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--platform", choices=list(PLATFORMS.keys()))
    args = ap.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    if not camo_ok():
        print("ERROR: Camofox not running. Start with:")
        print("  cd ~/Desktop/Oficina_Ranuk/_eval/camofox && npm start")
        sys.exit(1)
    print(f"Camofox OK. Scraping gigs for {today}...")

    platforms = [args.platform] if args.platform else list(PLATFORMS.keys())
    all_gigs = []
    stats = {}

    for pname in platforms:
        scraper = PLATFORMS[pname]
        count = 0
        for q in QUERIES:
            try:
                found = scraper(q)
                all_gigs.extend(found)
                count += len(found)
            except Exception as e:
                print(f"  X {pname}/{q}: {e}")
        stats[pname] = count
        print(f"  {pname}: {count} gigs found")

    # Deduplicate by URL
    seen = set()
    unique = []
    for g in all_gigs:
        key = g.get("url", "") or g.get("title", "")
        if key and key not in seen:
            seen.add(key)
            unique.append(g)
    all_gigs = unique

    # Sort by budget descending
    all_gigs.sort(key=lambda x: x.get("budget_max", 0), reverse=True)

    result = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "date": today,
        "total_gigs": len(all_gigs),
        "stats": stats,
        "min_budget_filter": MIN_BUDGET,
        "queries": QUERIES,
        "gigs": all_gigs,
    }

    if not args.dry_run:
        dated = OUT / f"gigs-{today}.json"
        combined = OUT / "all-gigs.json"
        with open(dated, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        with open(combined, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"
Saved {len(all_gigs)} gigs to:")
        print(f"  {dated}")
        print(f"  {combined}")
    else:
        print(f"
[DRY RUN] Would save {len(all_gigs)} gigs")

    # Print top 5
    if all_gigs:
        print("
=== TOP 5 GIGS ===")
        for i, g in enumerate(all_gigs[:5], 1):
            print(f"  {i}. [{g['platform']}] {g['title']}")
            print(f"     Budget: {g['budget']}  URL: {g['url'][:80]}")

    return result

if __name__ == "__main__":
    main()
