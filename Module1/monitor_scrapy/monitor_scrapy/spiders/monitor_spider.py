import scrapy
from monitor_scrapy.items import MonitorScrapyItem

class MonitorSpider(scrapy.Spider):
    name = "monitor"
    start_urls = ["https://ek.ua/ua/list/157/"]

    def parse(self, response):
        product_count = len(response.xpath('/html/body//*[@id="list_form1"]/child::*/div[contains(@class, "model-short-div")]'))
        for i in range(product_count):
            monitor = MonitorScrapyItem()
            monitor["model"] = response.xpath('/html/body//*[@id="list_form1"]/child::*/div[contains(@class, "model-short-div")]/table/tr/td[2]/table/tr/td[1]/a/@title').getall()[i]
            monitor["screen"] = response.xpath('/html/body//*[@id="list_form1"]/child::*/div[contains(@class, "model-short-div")]/table/tr/td[2]/div[1]/div[2]/div[1]/@title').getall()[i].split(",")[1]
            monitor["matrix"] = response.xpath('/html/body//*[@id="list_form1"]/child::*/div[contains(@class, "model-short-div")]/table/tr/td[2]/div[1]/div[2]/div[2]/@title').getall()[i].split(":")[1].replace("\xa0", "")
            monitor["functions"] = response.xpath('/html/body//*[@id="list_form1"]/child::*/div[contains(@class, "model-short-div")]/table/tr/td[2]/div[1]/div[2]/div[3]/@title').getall()[i].split(":")[1]
            monitor["connection_type"] = response.xpath('/html/body//*[@id="list_form1"]/child::*/div[contains(@class, "model-short-div")]/table/tr/td[2]/div[1]/div[2]/div[4]/@title').getall()[i].split(":")[1]
            yield monitor

        for i in range(2, 50): # go throught 50 pages
            yield response.follow(f'https://ek.ua/ua/list/157/{i}/', callback=self.parse)

     


    