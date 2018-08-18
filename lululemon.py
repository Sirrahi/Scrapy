from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json


class LululemonSpider(CrawlSpider):
    name = "lululemon"

    start_urls = (
        'https://shop.lululemon.com/',
    )

    listing_css = ['.item-types']
    product_css = ['.product-list']
    deny_r = ['/collections', '/community']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_item(self, response):
        raw_data = json.loads(response.css('script:contains(productData) ::text').extract_first()[27:])
        current_product_data = raw_data['rootReducer']['application']['currentProductContainer']['props']
        retailer_sku = current_product_data['productData']['product-summary']['default-sku']
        category = current_product_data['productData']['product-summary']['product-category']
        brand = current_product_data['translations']['seo']['copyright']['value']
        url = response.urljoin(current_product_data['match']['url'])
        retailer = current_product_data['translations']['seo']['ogTags']['siteName']
        name = current_product_data['productData']['product-summary']['product-name']
        description = current_product_data['productData']['product-summary']['why-we-made-this']
        price = current_product_data['productData']['price']['listPrice']
        currency = current_product_data['productData']['price']['currency']
        sku = current_product_data['productData']['child-skus']

        yield {
            'retailer_sku': retailer_sku,
            'category': category,
            'brand': brand,
            'url': url,
            'retailer': retailer,
            'name': name,
            'description': description,
            'price': price,
            'currency': currency,
            'sku': sku,
        }
