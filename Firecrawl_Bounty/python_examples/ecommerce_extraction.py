from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="YOUR_API_KEY")

# Advanced scraping with data extraction (JSON schema)
# This demonstrates the power of Firecrawl's LLM-based extraction
scrape_result = app.scrape_url(
    "https://example-ecommerce.com/products",
    params={
        "formats": ["json"],
        "json_options": {
            "schema": {
                "type": "object",
                "properties": {
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "price": {"type": "number"},
                                "in_stock": {"type": "boolean"}
                            }
                        }
                    }
                }
            }
        }
    }
)
print(scrape_result)