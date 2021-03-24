# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MonitorScrapyItem(scrapy.Item):
    model = scrapy.Field()
    screen = scrapy.Field()
    matrix = scrapy.Field()
    functions = scrapy.Field()
    connection_type = scrapy.Field()
    

