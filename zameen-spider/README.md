# Zameen Scraper

This is the scraper that I used to scrap 450K listings from Zameen.com over December 2020.

## Instructions
1. Clone this repo
2. Install scrapy into your virtual environment e.g. `conda install scrapy` 
3. Run the spider from root using `scrapy runspider zameen-spider/zameen/spiders/zameen-scraper.py`

Note: By default, the spider will scrap all listings and save it in root. You can modify these settings by going to the spider file (zameen-spider/zameen/spiders/zameen-spider.py) and updating `start_urls` and `path`.

## Resources
[Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)