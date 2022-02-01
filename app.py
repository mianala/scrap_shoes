# scrap shoes from https://www.moreschi.it/collections/heritage-shoes
import scrapy
from lxml import html


class MoreschiSpider(scrapy.Spider):
    name = "Moreschi Shoes"
    start_urls = ['https://www.moreschi.it/collections/heritage-shoes']

    def parse(self, response):
        # follow links to shoe pages
        for href in response.css('.ProductItem__ImageWrapper::attr(href)'):
            yield response.follow(href, self.parse_shoe)

        # follow pagination links
        for href in response.css('.Pagination__NavItem:last-child:not(.is-active)::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_shoe(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'title': extract_with_css('h1.ProductMeta__Title::text'),
            'price': extract_with_css('.ProductMeta__PriceList .ProductMeta__Price::text'),
            'description': extract_with_css('.ProductMeta__Description p::text') + extract_with_css('.ProductMeta__Description span::text'),
            # 'image': extract_with_css('img.product-card__image::attr(src)'),
            'url': response.url,
        }
