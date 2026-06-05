#!/usr/bin/env python3
"""Step 1: Write gigs data to JSON."""
import json, os
OUT = os.path.expanduser("~/Desktop/Oficina_Ranuk/freelance-gigs")
G = []
G.append({"t":"Kalshi Trading Bot Developer","p":"upwork","b":"$50-$180/hr","bm":180,"tp":"hourly","d":"Build automated trading bots on Kalshi (prediction markets). Python Flask + PostgreSQL. Strategy backtesting, fee/EV modeling.","r":"Kalshi/Polymarket trading exp, Python REST API, Kelly sizing, Claude","dl":"1-3mo","u":"https://www.upwork.com/nx/search/jobs/?q=kalshi+trading+bot","ms":95,"n":"PERFECT FIT - Polymarket bots + Python + API"})
G.append({"t":"AI Receptionist Agent","p":"upwork","b":"Hourly TBD","bm":80,"tp":"hourly","d":"End-to-end AI Receptionist: client comms, lead mgmt, scheduling. OpenAI, Airtable, n8n, Python, Gmail, Telegram APIs.","r":"AI agents, n8n, Python, Airtable, Gmail+Telegram APIs","dl":"<1mo","u":"https://www.upwork.com/nx/search/jobs/?q=AI+receptionist","ms":88,"n":"EXCELLENT - Python+AI+n8n+Telegram"})
G.append({"t":"Automation for File Download","p":"upwork","b":"$30-$60/hr","bm":60,"tp":"hourly","d":"Download historical data from insiderfinance.io. Automate with Playwright.","r":"Python, Playwright/Selenium, immediate","dl":"<1mo","u":"https://www.upwork.com/nx/search/jobs/?q=automation+download","ms":85,"n":"Quick win - Playwright"})
G.append({"t":"CRM Automation - Simpro & GoHighLevel","p":"upwork","b":"$15-$40/hr","bm":40,"tp":"hourly","d":"Integrate Simpro+GoHighLevel. ~20 SMS/email automations. Ongoing work.","r":"Simpro API, GoHighLevel, webhooks, n8n/Make","dl":"1-3mo","u":"https://www.upwork.com/nx/search/jobs/?q=CRM+automation","ms":80,"n":"Long-term client potential"})
G.append({"t":"Anti-AI Scraping Specialist","p":"upwork","b":"$30-$60/hr","bm":60,"tp":"hourly","d":"Protect e-commerce from AI scraping. Cloudflare Bot Management, rate limiting.","r":"Cloudflare, WAF, bot management","dl":"1-3mo","u":"https://www.upwork.com/nx/search/jobs/?q=anti+scraping","ms":75,"n":"Knows scraping attack vectors"})
G.append({"t":"Senior Automation & Security Consultant","p":"upwork","b":"$20-$70/hr","bm":70,"tp":"hourly","d":"20hr audit: NodeJS arch, API integrations, data pipelines, QA automation.","r":"Cybersecurity + QA automation, NodeJS","dl":"1-3mo","u":"https://www.upwork.com/nx/search/jobs/?q=automation+security","ms":70,"n":"20hr ~$1400 at $70/hr"})
G.append({"t":"Automate Agency Ops - AI Agents","p":"upwork","b":"$5-$40/hr","bm":40,"tp":"hourly","d":"Automate agency: acquisitions, emails, LinkedIn. AI agents for multiple roles.","r":"AI agents, business process automation","dl":"6mo+","u":"https://www.upwork.com/nx/search/jobs/?q=automate+agency","ms":72,"n":"Long-term, negotiate rate"})
G.append({"t":"AI Editorial Workflow (WordPress+n8n)","p":"freelancer","b":"$188 avg","bm":500,"tp":"fixed","d":"Content workflow: monitor sources, classify, score, draft. n8n + WordPress REST API + LLM.","r":"n8n/Make, API, scraping, LLM integration","dl":"6d","u":"https://www.freelancer.com/jobs/web-scraping","ms":82,"n":"scraping+n8n+WordPress"})
G.append({"t":"Business Website Lead Scraper","p":"freelancer","b":"$44 avg","bm":200,"tp":"fixed","d":"Scrape business websites for contacts: name, email, phone, address.","r":"Python, BeautifulSoup/Scrapy/Selenium","dl":"6d","u":"https://www.freelancer.com/jobs/web-scraping","ms":90,"n":"EASY WIN - fast delivery"})
G.append({"t":"Real Estate Data Extractor","p":"freelancer","b":"$198 avg","bm":600,"tp":"fixed","d":"Property data tool: address -> web crawl -> Google Sheets. FEMA, Zillow, county data.","r":"Python, Selenium, API, Google Maps","dl":"6d","u":"https://www.freelancer.com/jobs/web-scraping","ms":78,"n":"Modular scraping + APIs"})

# Expand gigs to full format
gigs = []
for g in G:
    gigs.append({
        "title": g["t"], "platform": g["p"], "budget": g["b"],
        "budget_max": g["bm"], "type": g["tp"], "description": g["d"],
        "requirements": g["r"], "deadline": g["dl"], "posted": "2026-06-05",
        "url": g["u"], "match_score": g["ms"], "notes": g["n"]
    })

import datetime
today = datetime.datetime.now().strftime("%Y-%m-%d")
result = {
    "scraped_at": "2026-06-05T08:17:00+02:00",
    "date": today, "total_gigs": len(gigs),
    "stats": {"upwork": 7, "freelancer": 3},
    "min_budget_filter": 200,
    "queries": ["automation bot", "scraping tool", "data pipeline", "API integration", "Python automation"],
    "gigs": gigs
}

dated = os.path.join(OUT, f"gigs-{today}.json")
combined = os.path.join(OUT, "all-gigs.json")
for p in [dated, combined]:
    with open(p, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Saved {len(gigs)} gigs to {dated}")
for i, g in enumerate(sorted(gigs, key=lambda x: x['match_score'], reverse=True)[:5], 1):
    print(f"  {i}. [{g['match_score']}%] {g['title']} ({g['platform']}) - {g['budget']}")
