import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QuotesSpider(CrawlSpider):
    name = "msgm"
    start_urls = [
        'https://www.msgm.it/en/',
    ]

    listing_css = ['div[id=menu_links] ul[class!=marginTop30]', 'div[id=menu_links]']
    product_css = ['div.vaschetta_item_img']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        retailer_sku = response.css('div.details_info_code ::text').extract_first()
        if retailer_sku:
            retailer_sku = re.search(r'\d.+', retailer_sku.strip()).group()
        gender = response.css('div.details_info_back a ::text').extract_first()
        category = response.css('div.details_info_back a ::text').extract()[1]
        brand = response.css('script:contains(price) ::text').extract_first()
        if brand:
            brand = re.search("'brand':'(\w+)'", brand).group(1)
        url = response.url
        retailer = response.css('div.header_sx a ::attr(title)').extract_first()
        name = response.css('div.details_info_title h1 ::text').extract_first()
        description = response.css('div.details_info_descr ::text').extract_first().strip()
        if not description:
            description = response.css('div.details_info_descr p ::text').extract_first().strip()
        image_urls = response.css('div.details_block_50 a.MagicZoom ::attr(href)').extract()
        currency = response.css('div.details_info_price meta ::attr(content)').extract_first()
        new_price = response.css('div.details_price_new span ::text').extract_first()
        if new_price:
            new_price = re.search(" (.+) ", new_price).group(1)
        item_size_list = response.css('select.general_select_100 option ::text').extract()
        old_price = response.css('div.details_price_old ::text').extract_first()
        if old_price:
            old_price = re.search(" (.+) ", old_price).group(1)

        items = {
            'retailer_sku': retailer_sku,
            'gender': gender,
            'category': category,
            'brand': brand,
            'url': url,
            'retailer': retailer,
            'name': name,
            'description': description,
            'image_urls': image_urls,
            'sku': []
        }

        for size in item_size_list:
            items['sku'].append({'size': size, 'new_price': new_price, 'old_price': old_price, 'currency': currency})

        yield items
