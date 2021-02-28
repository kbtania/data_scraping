# -*- coding: utf-8 -*-
import scrapy


class LibrarySpider(scrapy.Spider):
    name = 'library'
    allowed_domains = ['irbis-nbuv.gov.ua']
    start_urls = ['http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_n'
                  'buv/cgiirbis_64.exe?S21CNR=1000&S21STN=1&S21REF='
                  '2&C21COM=S&I21DBN=UJRN&P21DBN=UJRN&S21All=%3C.%3EJJA%3DA'
                  '$%3C.%3E&S21FMT=j_brief&Z21ID=&S21SRW=nz']

    def get_cities(self, response):
        books = response.xpath('/html/body/table[1]/tr[4]/td[2]/table[2]/table[2]')
        to = len(books[0].css('tr td::text'))
        cities = []
        for i in range(5, to, 2):
            cities.append(books[0].css('tr td::text')[i].getall()[0][2:])
        return cities

    def parse(self, response):
        books = response.xpath('/html/body/table[1]/tr[4]/td[2]/table[2]/table[2]')
        count = len(books[0].css('tr td a::attr(href)'))
        for i in range(count):
            yield {
                'name': books[0].css('tr td a::text')[i].getall()[0],
                'city': self.get_cities(response)[i],
                'link': books[0].css('tr td a::attr(href)')[i].getall()
            }
        letters = 'ABCDEFGHIJLMOPRSTUVWАБВГДЕЄЖЗИІКЛМНОПРСТУФХЦЧШЭЮЯ'  # for links
        for i in range(1, len(letters)):
            yield response.follow(f'http://www.irbis-nbuv.gov.ua/cgi-bin/irbis_nbuv/cgiirbis_64.exe?S21CNR='
                                  f'1000&S21STN=1&S21REF=2&C21COM=S&I21DBN=UJRN&P21DBN=UJRN&S21All=%3C.%3EJJA%3D'
                                  f'{letters[i]}$%3C.%3E&S21FMT=j_brief&Z21ID=&S21SRW=nz', callback=self.parse)



