import scrapy
from scrapy.http import HtmlResponse

class LabirintruSpider(scrapy.Spider):
    name = "labirintru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/books"]

    def parse(self, response):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@class='genres-catalog']//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        old_price = float(response.xpath("//span[@class='buying-priceold-val-number']/text()").get())
        new_price = float(response.xpath("//span[@class='buying-pricenew-val-number']/text()").get())
        url = response.url
        yield {'name': name,
               'old_price': old_price,
               'new_price': new_price,
               'url': url}