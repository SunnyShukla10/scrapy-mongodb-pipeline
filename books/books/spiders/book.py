import scrapy
from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = BooksItem()
            item['url'] = book.css("h3 > a::attr(href)").get()
            item['name'] = book.css("h3 > a::attr(title)").get()
            item['price'] = book.css(".price_color::text").get()
            yield item
        
        # Target the href to get the next pages
        next_page = response.css('li.next > a::attr(href)').get()
        
        # The url isn't a qualified URL so you its needed to combine with the base URL before scrapy sends a request
        #    urljoin does that for you and this is done recursively until no more next links are left
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)