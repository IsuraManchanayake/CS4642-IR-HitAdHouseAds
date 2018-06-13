import scrapy


class HouseSpider(scrapy.Spider):
    name = 'houses'
    start_urls = ['http://www.hitad.lk/EN/property?page=0']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for house in response.css('ul.cat-ads'):
            if house.css('h4.fw_b'):
                item = {
                    'title': house.css('h4.fw_b::text').extract_first().strip(),
                    'link' : house.css('a').extract_first().strip(),
                    'date': '',
                    'type': '',
                    'location': '',
                    'category': '',
                    'property_type': '',
                    'sub_category': '',
                    'price': '',
                    'ref': ''
                }
                yield item
