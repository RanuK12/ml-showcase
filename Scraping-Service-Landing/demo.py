#!/usr/bin/env python3
"""Ranukita Scraping API - Demo Script. Usage: python demo.py"""
import requests, json, csv, time
from datetime import datetime

API_KEY = "rk_live_your_key_here"
BASE_URL = "https://api.ranuk.dev/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def scrape_products(target_url, max_pages=3):
    print(f"\n🔍 Scraping: {target_url} (max {max_pages} pages)")
    print("-" * 60)
    payload = {
        "target": target_url, "format": "json",
        "fields": ["name","price","original_price","rating","reviews"],
        "pagination": True, "max_pages": max_pages
    }
    # In production: resp = requests.post(f"{BASE_URL}/scrape", headers=HEADERS, json=payload)
    data = {
        "status": "success", "request_id": "req_8f3k2j1n",
        "pages_scraped": 3, "results_count": 6, "elapsed_ms": 4200,
        "results": [
            {"name":"Wireless Headphones","price":79.99,"original_price":129.99,"rating":4.7,"reviews":2341},
            {"name":"Smart Watch Pro","price":199.99,"original_price":249.99,"rating":4.5,"reviews":1892},
            {"name":"USB-C Hub 7-in-1","price":34.99,"original_price":49.99,"rating":4.8,"reviews":567},
            {"name":"Ergonomic Chair","price":299.00,"original_price":399.00,"rating":4.3,"reviews":891},
            {"name":"4K Webcam","price":89.99,"original_price":119.99,"rating":4.6,"reviews":1203},
            {"name":"Mech Keyboard RGB","price":129.99,"original_price":159.99,"rating":4.9,"reviews":3456},
        ]
    }
    print(f"✅ {data['pages_scraped']} pages, {data['results_count']} products, {data['elapsed_ms']}ms\n")
    for i, p in enumerate(data["results"], 1):
        disc = round((1 - p["price"]/p["original_price"])*100)
        print(f"  {i}. {p['name']}")
        print(f"     ${p['price']:.2f} (was ${p['original_price']:.2f}, -{disc}%)")
        print(f"     ⭐ {p['rating']}/5 | {p['reviews']:,} reviews\n")
    return data["results"]

def monitor_prices(urls):
    print(f"\n📊 Price Monitor — {len(urls)} products")
    print("-" * 60)
    for url in urls:
        price, was = 79.99, 99.99
        change = round((price - was) / was * 100, 1)
        print(f"  {'📉' if change < 0 else '➡️'} {url}")
        print(f"     ${price:.2f} (was ${was:.2f}, {change:+.1f}%) — In Stock\n")

def export_csv(products, fname="ranukita_products.csv"):
    with open(fname, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name","price","original_price","rating","reviews"])
        w.writeheader()
        w.writerows(products)
    print(f"💾 Exported {len(products)} products to {fname}")

if __name__ == "__main__":
    print("=" * 60)
    print("  🕷️  RANUKITA SCRAPING API — DEMO")
    print(f"  📅  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    products = scrape_products("https://example-store.com/electronics")
    monitor_prices([
        "https://example-store.com/products/headphones",
        "https://example-store.com/products/smartwatch"
    ])
    export_csv(products)
    print("\n🎉 Done! Visit ranuk.dev to get your API key.")
