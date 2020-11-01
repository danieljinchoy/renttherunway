from scrapy import Spider, Request
from renttherunway.items import RenttherunwayItem
import re

class renttherunwaySpider(Spider):
    name = 'renttherunway_spider'
    start_urls = ['https://www.renttherunway.com/c/dresses?filters%5Bzip_code%5D=08901&sort=recommended#1604176344889']
    allowed_urls = ['https://www.renttherunway.com/']


    def parse(self, response):
        num_pages = 131

        url_list = [f'https://www.renttherunway.com/c/dresses?filters%5Bzip_code%5D=08901&sort=recommended&page={i}&_=1604176342590#1604177185813' 
                    for i in range(1, num_pages + 1)]

        for url in url_list[:3]:

            # For debugging
            # print('='*55)
            # print(url)
            # rpint('='*55)


            yield Request(url=url, callback=self.)


    def parse_result_page(self, response):
        pass 


