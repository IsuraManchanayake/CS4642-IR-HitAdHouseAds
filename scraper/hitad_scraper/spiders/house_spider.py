import scrapy
import logging

class HouseAdItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    item_type = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    property_type = scrapy.Field()
    description = scrapy.Field()

class HouseSpider(scrapy.Spider):
    name = 'houses'
    start_urls = ['http://www.hitad.lk/EN/property']
    page = 0

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.ERROR)
        super(HouseSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        for house in response.css('ul.cat-ads>li div.row'):
            if house.css('h4.fw_b'):
                house_ad = HouseAdItem()
                house_ad['title'] = house.css('h4.fw_b::text').extract_first().strip()
                house_ad['link'] = house.css('a::attr(href)').extract_first().strip()
                house_ad['date'] = house.css('div.ad-info-2::text').extract_first()[7:].strip()
                house_ad['item_type'] = house.css('div.item-facets::text')[0].extract().strip()
                house_ad['category'] = house.css('div.item-facets::text')[1].extract().strip()
                house_ad['sub_category'] = house.css('div.item-facets::text')[2].extract().strip()
                house_ad['location'] = (lambda x: '-' if len(x) < 1 else x[0].extract().strip())(house.css('div.item-facets2::text'))
                house_ad['property_type'] = (lambda x: '-' if len(x) < 4 else x[3].extract().strip())(house.css('div.item-facets::text'))
                house_ad['price'] = (lambda x: int(x[4:].replace(',','')) if x.startswith('Rs') else x)(house.css('span.list-price-value::text')[0].extract())

                description_request = scrapy.Request(house_ad['link'], callback=self.parse_description_page)
                description_request.meta['house_ad'] = house_ad
                yield description_request
        self.page += 25
        next_page_url = self.start_urls[0] + '?page=' + str(self.page)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_description_page(self, response):
        house_ad = response.meta['house_ad']
        house_ad['description'] = " ".join(response.xpath('//div[@class="mar_t_20"]/p/text()').extract())
        yield house_ad
