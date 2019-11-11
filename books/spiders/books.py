# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    # allowed_domains = ["books.toscrape.com"]
    allowed_domains = ["www.bukalapak.com"]
    # start_urls = [
    #     'http://books.toscrape.com/',
    # ]
    start_urls = [
        'https://www.bukalapak.com/products/s/earphone-bass',
    ]

    def parse(self, response):
        for book_url in response.css("div.o-layout__item.product-description > h3 > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("a.next_page ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        product = response.css("div.o-layout__item.u-8of12.u-position-relative")
        item["title"] = product.css("h1 ::text").extract_first()
        # item['category'] = response.xpath(
        #     "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        # ).extract_first()
        item['category'] = response.xpath(
            "//ul[@class='c-breadcrumb']/li[@class='c-breadcrumb__item']/preceding-sibling::li[1]/a/text()"
        ).extract_first()
        item['description'] = response.xpath(
            "//div[@id='rmjs-2']/following-sibling::p/text()"
        ).extract_first()
        # item['description'] = response.xpath(
        #     "//div[@id='product_description']/following-sibling::p/text()"
        # ).extract_first()
        item['price'] = response.css('div.c-product-detail-price__reduced > span.amount.positive::text').extract_first()
        yield item
