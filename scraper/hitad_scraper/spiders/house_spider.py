import scrapy
import logging

class HouseAdItem(scrapy.Item):
    """
        The house advertisement Item to structure data
    """
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
    """
        House advertisement scraper
    """
    name = 'houses'
    start_urls = ['http://www.hitad.lk/EN/property']
    page = 0

    def __init__(self, *args, **kwargs):
        """
            Overloaded __init__ method to log errors in to a seperate file. The scrape command should 
            contain the flag --logfile 'filename'
        """
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.ERROR)
        super(HouseSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
            Parses the listing page
        """
        for house in response.css('ul.cat-ads>li div.row'):
            if house.css('h4.fw_b'):
                house_ad = HouseAdItem()
                house_ad['title'] = house.css('h4.fw_b::text').extract_first().strip()
                house_ad['link'] = house.css('a::attr(href)').extract_first().strip()
                house_ad['date'] = house.css('div.ad-info-2::text').extract_first()[7:].strip()
                house_ad['item_type'] = house.css('div.item-facets::text')[0].extract().strip()
                house_ad['category'] = house.css('div.item-facets::text')[1].extract().strip()
                house_ad['sub_category'] = house.css('div.item-facets::text')[2].extract().strip()
                house_ad['location'] = (lambda x: '-' if len(x) < 1 else x[0].extract().strip()) \
                    (house.css('div.item-facets2::text')) # "-" if there are no location data
                house_ad['property_type'] = (lambda x: '-' if len(x) < 4 else x[3].extract().strip()) \
                    (house.css('div.item-facets::text')) # "-" if there are no property_type data
                house_ad['price'] = (lambda x: int(x[4:].replace(',','')) if x.startswith('Rs') else x) \
                    (house.css('span.list-price-value::text')[0].extract()) # Some ads contain the price while others have marked as "Negotiable" 

                # Requesting the description page by passing the house_ad object as meta
                description_request = scrapy.Request(house_ad['link'], callback=self.parse_description_page)
                description_request.meta['house_ad'] = house_ad
                yield description_request
        
        # Requesting the next listing page
        self.page += 25
        next_page_url = self.start_urls[0] + '?page=' + str(self.page)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_description_page(self, response):
        """
            Parses the description page. house_ad object should be included in the request object
        """
        house_ad = response.meta['house_ad']
        house_ad['description'] = " ".join(response.xpath('//div[@class="mar_t_20"]/p/text()').extract())
        yield house_ad
