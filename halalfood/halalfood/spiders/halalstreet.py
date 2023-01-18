import scrapy
from ..items import HalalfoodItem


class HalalstreetSpider(scrapy.Spider):
    name = 'halalstreet'
    start_urls = ['https://www.halalstreet.co.uk/product-category/malaysian-product/']
    page_numb = 2

    def parse(self, response):
        items = HalalfoodItem()
        contents = response.css('div.content-product')
        for content in contents:
            product_title = content.css('.product-title a::text').get()
            product_price = content.css('ins span bdi::text').get()
            if product_price is None:
                product_price = content.css('span.price span bdi::text').get()
            product_rating = content.css('strong.rating::text').get()

            items['product_name'] = product_title
            items['product_price'] = product_price
            items['product_rating'] = product_rating

            yield items

        next_page = 'https://www.halalstreet.co.uk/product-category/malaysian-product/page/' + str(HalalstreetSpider.page_numb)
        if HalalstreetSpider.page_numb <= 59:
            HalalstreetSpider.page_numb += 1
            yield response.follow(next_page, callback=self.parse)
