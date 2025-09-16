# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    _id = scrapy.Field() # _id fields when the item pipelie adds the value for ._id after calculating hashval from .url 
    url = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
