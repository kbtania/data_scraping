import scrapy
from lab3_scrapy.items import HotlineScraperItem

class VideocardsSpider(scrapy.Spider):
    name = "videocards"
    start_urls = ['https://hotline.ua/computer/videokarty/']

    def parse(self, response):
        products = response.css('li.product-item') # all videocards
        for product in products:
            try:
                videocard = HotlineScraperItem()
                videocard["name"] = product.css('div.item-info p a::text').get().strip('\n').replace('    ', '').rstrip()
                videocard["price"] = product.css('div.price-md span::text').get().replace('\xa0', ' ')
                videocard["link"] = 'hotline.ua' + product.css('p.h4 a::attr(href)').get()
                yield videocard
            except AttributeError:
                pass
        next_page = response.css('a.next ::attr(href)').get()
        if next_page is not None:
            yield response.follow(self.start_urls[0]+next_page, callback=self.parse)