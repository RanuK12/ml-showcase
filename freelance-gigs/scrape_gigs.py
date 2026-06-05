#!/usr/bin/env python3
# © 2026 Ranuk IT Solutions — ranuk.dev
"""Scrapes freelance platforms for automation gigs via Camofox stealth browser."""
import json, os, re, sys, time, urllib.request, subprocess
from datetime import datetime

CAMO = "http://127.0.0.1:9377"
DIR = os.path.dirname(os.path.abspath(__file__))
QUERIES = ["automation bot", "scraping tool", "data pipeline", "API integration", "Python automation"]
PLATFORMS = {
    "upwork": {"name":"Upwork","urls":["https://www.upwork.com/nx/search/jobs/?q={q}&sort=recency"]},
    "freelancer": {"name":"Freelancer","urls":["https://www.freelancer.com/search/projects?q={q}&status=open"]},
    "fiverr": {"name":"Fiverr","urls":["https://www.fiverr.com/search/gigs?query={q}&source=category_tree&search_in=buying"]},
    "contra": {"name":"Contra","urls":["https://contra.com/opportunities?q={q}"]},
}

def camo_req(method, path, body=None, timeout=30):
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(CAMO+path, data=data, method=method, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return json.loads(resp.read())

def ensure_camofox():
    try:
        urllib.request.urlopen(CAMO+"/health", timeout=3); return True
    except: pass
    d = os.path.expanduser("~/Desktop/Oficina_Ranuk/_eval/camofox")
    subprocess.Popen(["/opt/homebrew/bin/npm","start"],cwd=d,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for _ in range(20):
        time.sleep(1.5)
        try: urllib.request.urlopen(CAMO+"/health",timeout=3); return True
        except: pass
    return False

def browse(url):
    s = {"userId":"ranukita","sessionKey":"ranukita"}
    tab = camo_req("POST","/tabs",s)
    tid = tab.get("tabId") or tab.get("id") or tab.get("tab",{}).get("id")
    camo_req("POST",f"/tabs/{tid}/navigate",{**s,"url":url})
    time.sleep(4)
    try: snap = camo_req("GET",f"/tabs/{tid}/snapshot?userId=ranukita&format=text")
    except: snap = {"snapshot":""}
    try: camo_req("DELETE",f"/tabs/{tid}?userId=ranukita")
    except: pass
    return snap.get("snapshot","")[:15000]

def parse_budget(t):
    m = re.search(r"\$[\d,]+(?:\.\d{2})?(?:\s*[-–]\s*\$[\d,]+)?", t)
    if m:
        nums = re.findall(r"[\d,]+\.?\d*", m.group(0))
        if nums: return max(float(n.replace(",","")) for n in nums)
    m = re.search(r"(?:budget|price)[:\s]*\$?([\d,]+)", t, re.I)
    if m: return float(m.group(1).replace(",",""))
    return None

def extract_gigs(snap, platform, query):
    gigs, lines = [], snap.split("\n") if snap else []
    for i,ln in enumerate(lines):
        ln = ln.strip()
        if not ln or len(ln)<10 or len(ln)>200 or ln.startswith("http") or ln.startswith("$"): continue
        kws = ["auto","bot","scrap","pipeline","api","python","data","integrat","script","tool","develop","build","web","app","system","software","engineer","project","hire","expert"]
        if any(k in ln.lower() for k in kws):
            ctx = "\n".join(lines[max(0,i-2):i+5])
            gigs.append({"title":ln[:150],"platform":platform,"query":query,
                         "budget":parse_budget(ctx),"deadline":None,"description":ctx[:500]})
    return gigs

def scrape_all(min_budget=200):
    if not ensure_camofox():
        print("⚠ Camofox no disponible"); return []
    all_gigs, seen = [], set()
    for pk,pc in PLATFORMS.items():
        for q in QUERIES:
            for ut in pc["urls"]:
                url = ut.format(q=q.replace(" ","+"))
                print(f"  🔍 {pc['name']}: {q}")
                try:
                    for g in extract_gigs(browse(url), pc["name"], q):
                        t = g["title"].lower().strip()
                        if t not in seen: seen.add(t); all_gigs.append(g)
                except Exception as e: print(f"    ⚠ {e}")
                time.sleep(2)
    filtered = [g for g in all_gigs if g["budget"] is None or g["budget"] >= min_budget]
    print(f"\n📊 {len(all_gigs)} total, {len(filtered)} budget >= ${min_budget}")
    return filtered

if __name__ == "__main__":
    date = datetime.now().strftime("%Y-%m-%d")
    mb = 200
    print(f"🚀 Ranukita Gigs Scraper — {date}\n")
    gigs = scrape_all(min_budget=mb)
    gigs.sort(key=lambda g: g["budget"] or 0, reverse=True)
    out = os.path.join(DIR, f"gigs-{date}.json")
    with open(out,"w") as f: json.dump({"date":date,"min_budget":mb,"total":len(gigs),"gigs":gigs}, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Guardado: {out} ({len(gigs)} gigs)")
    for g in gigs[:5]:
        print(f"  💼 {g['platform']}: {g['title'][:60]} | ${g['budget'] or '?'}")
