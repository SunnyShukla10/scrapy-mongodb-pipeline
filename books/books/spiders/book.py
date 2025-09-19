import scrapy
from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.log_error,  # handle errors on first request
            )

    def parse(self, response):

        # (@url) specifies the url to test the parse method
        # first (@returns) specifies that the min number of items should be 20 per request and max is 20 
        # second (@returns) specifies that the .parse() method generate at least 1 and at most 50 requests
        # (@scrapes) specifies that each returned item should have url, items, and price
        """
        @url https://books.toscrape.com
        @returns items 20 20
        @returns request 1 50
        @scrapes url name price
        """
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
            self.logger.info(f"Going to the next page {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse, errback=self.log_error)
    

    # a function to log and handle errors 
    def log_error(self, faliure):
        self.logger.error(repr(faliure)) # return the error in a developer-friendly format