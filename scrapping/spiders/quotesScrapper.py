import scrapy
from scrapping.items import QuoteItem


class QuotesscrapperSpider(scrapy.Spider):
    name = "quotesScrapper"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    custom_settings = {
        "DOWLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS": 1,
        "FEED_URI": "D:\Repo\scrappyTutorial\data\quotes.json",
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "LOG_LEVEL": "INFO",
    }

    def parse(self, response):
        self.logger.info("Scrapping page: %s", response.url)
        quotes = response.css("div.quote")
        item = QuoteItem()

        for quote in quotes:
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("small.author::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
