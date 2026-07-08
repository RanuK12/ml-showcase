from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="YOUR_API_KEY")

# Simple scrape of a website
scrape_result = app.scrape_url("https://example.com")
print(scrape_result)