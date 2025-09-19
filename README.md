# Scrapy + MongoDB Books Scraper

## Overview
This is a small side project I built to learn more about **web scraping** and **NoSQL databases**.  
The scraper extracts book information from [Books to Scrape](https://books.toscrape.com/) and stores it in **MongoDB** using a Scrapy pipeline.

## Tools
- **Scrapy** – Fast, high-level scraping framework for Python
- **MongoDB** – Open-source NoSQL database with flexible schema and easy horizontal scalability

## Data
From [Books to Scrape](https://books.toscrape.com/), the scraper collects:
- Title  
- Price  
- Rating  
- URL  

Pagination is handled so the spider crawls through all pages of the site.

## How It Works
1. **Inspect website structure** using Scrapy Shell and CSS selectors.  
2. **Define Items** in `items.py` to structure the scraped data.  
3. **Build Spider** in `spiders/` with `.parse()` for extracting book info and following next-page links.  
4. **Use Pipelines** in `pipelines.py` to store items into MongoDB (`books_db`).  
5. **Error Handling** with custom `errback` methods and `start_requests()` for robust crawling.  

## Notes
- Pipelines also handle duplicates by creating unique IDs.  
- Logging with `LOG_LEVEL` helps with debugging.  
- Contracts can be used to embed test cases directly in spiders.  

---

This was mainly a **learning project** to practice:
- Web scraping with Scrapy  
- Handling pagination & request errors  
- Working with MongoDB as a storage backend  
- Using pipelines for ETL-like workflows  