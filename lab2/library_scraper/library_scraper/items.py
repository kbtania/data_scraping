# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LibraryScraperItem(scrapy.Item):
    name = scrapy.Field()
    city = scrapy.Field()
    link = scrapy.Field()

class HotlineScraperItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    
