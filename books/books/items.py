# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    url = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
