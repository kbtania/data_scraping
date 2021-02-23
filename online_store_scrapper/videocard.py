import scrapy


class VideocardSpider(scrapy.Spider):
    name = 'videocard'
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/computer/videokarty/']


    def parse(self, response):
        products = response.css('li.product-item')
        for product in products:
            try:
                yield {
                    'name': product.css('div.item-info p a::text').get().strip('\n').replace('    ', ''),
                    'price': product.css('div.price-md span::text').get().replace('\xa0', ' '),
                    'link': 'hotline.ua' + product.css('p.h4 a::attr(href)').get(),
                    #  'quantity': product.css('div.stick-pull div a::text').get()
                }
            except AttributeError:
                pass
        next_page = response.css('a.next ::attr(href)').get()
        if next_page is not None:
            yield response.follow(self.start_urls[0]+next_page, callback=self.parse)

# scrapy runspider videocard.py -O [filename].csv
