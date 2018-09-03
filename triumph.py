import json
import re

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import Item


class Triumph(CrawlSpider):
    name = 'triumph'

    start_urls = (
        'http://uk.triumph.com/',
    )

    listing_css = ['.mainMenu-holder', '.pagination-wrapper']
    product_css = ['.productgrid .thumbnail']
    deny_r = ['/en_uk']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_item(self, response):
        skus = {}
        image_urls = []
        item = ItemLoader(item=Item(), response=response)

        raw_product = self.raw_product(response)
        color_urls = self.color_urls(response)

        item.add_value('retailer_sku', self.retailer_sku(raw_product))
        item.add_value('name', self.product_name(raw_product))
        item.add_value('color', self.color(raw_product))
        item.add_value('retailer', self.retailer(raw_product))
        item.add_value('brand', self.brand(raw_product))
        item.add_value('category', self.category(raw_product))
        item.add_value('description', self.description(response))

        for i in range(0, len(color_urls)):
            color_url = response.urljoin(color_urls[i])
            yield scrapy.Request(url=color_url, callback=self.parse_sizes,
                                 meta={'skus': skus, 'image_urls': image_urls,
                                       'color_urls': color_urls, 'item': item})

    def parse_sizes(self, response):
        color_urls = response.meta['color_urls']

        sizes = self.sizes(response)
        color = self.sku_color(response)
        price = self.sku_price(response)
        currency = self.sku_currency(response)
        image_urls_each_color = self.image_urls_each_color(response)

        self.image_urls(response, image_urls_each_color)
        self.skus(response, sizes, color, price, currency, image_urls_each_color)
        self.color_url_pop(color_urls)

        if len(color_urls) == 0:
            item = response.meta['item']
            item.add_value('image_urls', response.meta['image_urls'])
            item.add_value('skus', response.meta['skus'])

            yield {
                'item': item.load_item()
            }

    def image_urls_each_color(self, response):
        return response.css('.mainimageContainer img ::attr(src)').extract()

    def clean(self, text):
        return text.strip()

    def color_url_pop(self, color_urls):
        color_urls.pop()

    def skus(self, response, sizes, color, price, currency, image_urls_each_color):
        skus = response.meta['skus']
        sku = {}
        for size in sizes:
            sku[color + '-' + self.clean(size)] = {'color': color, 'size': self.clean(size),
                                                   'price': price, 'currency': currency,
                                                   'image_urls': image_urls_each_color}
            skus.update(sku)

    def image_urls(self, response, image_urls_each_color):
        image_urls = response.meta['image_urls']
        image_urls.append(image_urls_each_color[0])
        return image_urls

    def sku_currency(self, response):
        currency = response.css('.col .hide span[itemprop=priceCurrency] ::text').extract_first()
        return currency

    def sku_price(self, response):
        price = response.css('.col .hide span ::attr(content)').extract_first()
        return price

    def sku_color(self, response):
        color = self.clean(response.css('.colorsizes_mobileselect .nonFunctionalLink ::text').extract_first())
        return color

    def sizes(self, response):
        return response.css('.col .colorsizes_inner .overlaysizes li a ::text').extract()

    def color_urls(self, response):
        color_urls = response.css('.colorsizes_inner .colorswatch a ::attr(href)').extract()
        color_urls.append(response.css('.colorsizes_inner .selected a ::attr(href)').extract_first())
        return color_urls

    def description(self, response):
        return self.clean(('.'.join(response.css('.description ::text').extract())))

    def category(self, raw_product):
        return raw_product['productCategory']

    def brand(self, raw_product):
        return raw_product['ecommerce']['detail']['products'][0]['brand']

    def retailer(self, raw_product):
        return raw_product['ecommerce']['detail']['products'][0]['brand']

    def color(self, raw_product):
        return raw_product['productRealColor']

    def raw_product(self, response):
        raw_product = response.css('script:contains(productRealColor) ::text').extract_first()
        return json.loads(re.search(r'{.+}', raw_product).group())['googletagmanager']['data']

    def product_name(self, raw_product):
        return raw_product['productName']

    def retailer_sku(self, raw_product):
        return raw_product['productID']
