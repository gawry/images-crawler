# Installing the crawler
`poetry install` (Install poetry first if needed `pip install poetry`)

# Running the crawler
`scrapy crawl freeimages -a keyword=dogs`

# Running tests
pytest --reactor=asyncio .