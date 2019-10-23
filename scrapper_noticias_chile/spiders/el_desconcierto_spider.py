import scrapy
from ..items import NewsItem
import datetime
MAX_PAGES = 18


class ElDesconciertoSpider(scrapy.Spider):
    name = 'el_desconcierto'
    start_urls = [
        'https://www.eldesconcierto.cl/noticias/pais/',
    ]

    def parse(self, response):
        current_page_index = int(response.css('.page-numbers.current::text').get())
        next_page = response.css('.next.page-numbers::attr(href)').get()
        next_page_index = current_page_index + 1

        category = response.request.url.split("/")[4]
        response.meta['category'] = category
        response.meta['current_page_index'] = current_page_index

        for item in self.parse_index(response):
            yield item

        if next_page is not None and next_page_index <= MAX_PAGES:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_index(self, response):
        """Parse and process a news index page (a pages that shows a list of links to the news items).
        """

        if (response.meta['current_page_index'] > 1):
            news_item_links = response.css('.listado-estandar').css('.titulares')

        else:
            news_item_links = response.css('.categoria-abajo.clearfix').css('.titulares')

        for news_item_link in news_item_links:

            # Create the news item object, wich will store the processed new item:
            news_item = NewsItem()

            # Add the link and the category to the new item
            link_to_content = news_item_link.css('a::attr(href)').get()
            news_item["link"] = link_to_content

            # Add the category from the link of the news index
            news_item["category"] = response.meta['category']

            # Request and process the new
            content_request = scrapy.Request(link_to_content, callback=self.parse_content, dont_filter=True)
            content_request.meta["news_item"] = news_item

            yield content_request

    def parse_content(self, response):
        """Parse and process a specific news item. 
        """

        news_item = response.meta['news_item']

        # Add title and subtitle
        news_item["title"] = response.css('h1::text').get()
        news_item["subtitle"] = response.css('h2::text').get()

        # Add author
        news_item["author"] = response.css('span.autor')[0].css('a::text').get()
        news_item["author_link"] = response.css('span.autor')[0].css('a::attr(href)').get()
        news_item["author_twitter"] = response.css('a.autor-twitter::text').get()

        # Add date
        date = response.css('.fecha::text').get()
        date = date.strip()[2:].split('.')
        news_item["publication_date"] = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))

        # Add content processing
        content_list = response.css('.post-content').css('p::text').getall()
        news_item["content"] = ''.join(content_list)

        # Add tags
        news_item["tags"] = response.css('.tags').css('a::text').getall()
        news_item['tags_links'] = response.css('.tags').css('a::attr(href)').getall()

        yield news_item
