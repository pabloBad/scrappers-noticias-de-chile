import scrapy
from validators import url
from ..items import NewsItem

MAX_PAGES = 2000

NAME = "biobio"

START_URLS = ['https://www.biobiochile.cl/lista/tags/crisis-en-chile']


class BiobioSpider(scrapy.Spider):
    name = NAME
    start_urls = START_URLS

    def parse(self, response):
        current_page = 0

        for item in self.parse_index(response):
            yield item

        current_page = int((response.css(".small-content > p:nth-child(22)::text").get().split(" ")[2]))
        next_page = response.css("li.page-item:nth-child(13) > a:nth-child(1)::attr(href)").get()

        if next_page is not None and current_page < MAX_PAGES:
            next_page = response.urljoin(next_page)
            current_page += 1
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_index(self, response):

        for item in response.css("div.noticia.row"):

            news_item = NewsItem()

            link_to_content = item.css("div.col-xs-6.titular-fecha a::attr(href)").get()

            news_item["publication_date"] = item.css("div.col-xs-2.fecha p::text").get()
            news_item["publication_hour"] = item.css("div.col-xs-2.fecha span::text").get()
            news_item["author"] = item.css("p.autor a::text").get()
            news_item["author_link"] = item.css("p.autor a::attr(href)").get()
            news_item["title"] = item.css("div.col-xs-6.titular-fecha a h1::text").get()
            news_item["link"] = link_to_content

            content_request = scrapy.Request(link_to_content, callback=self.parse_content, dont_filter=True)
            content_request.meta["news_item"] = news_item

            yield content_request

    def parse_content(self, response):
        biobio_item = response.meta['news_item']

        # Content Processing

        # Get all data in the content
        content_list = response.css("div.nota-contenido.text-19.robotos *::text").getall()

        # Delete Gallery
        content_list = self.delete_gallery(content_list)

        # Delete tags
        content_list = self.delete_tags(content_list)

        # Delete banners
        content_list = self.delete_banners(content_list)

        # Join and delete embbebed URL
        content = "".join([
            text.strip() + " " if text.strip() != "" else " "
            for text in content_list
            if not url(text) and text != 'Lee también...'
        ])

        # Get document tags
        tags = [text.strip() for text in response.css("div.nota-etiquetas *::text").getall() if text.strip() != ""]
        # Delete 'Etiquetas de esta nota:'
        if len(tags) > 1:
            tags = tags[1:]

        # Categories and subcategories
        url_array = response.request.url.split("/")

        biobio_item["category"] = url_array[4]
        biobio_item["subcategory"] = url_array[5]
        biobio_item["content"] = content
        biobio_item["tags"] = tags
        biobio_item["embedded_links"] = [link for link in content_list if url(link)]

        yield biobio_item

    def delete_gallery(self, content_list):
        contains_gallery = [True if '\n\t#lightgallery' in text else False for text in content_list]
        try:
            gallery_index = contains_gallery.index(True)
        except ValueError:
            gallery_index = len(content_list) - 1

        return content_list[:gallery_index]

    def delete_tags(self, content_list):
        contains_tags = [True if 'Etiquetas de esta nota:' in text else False for text in content_list]
        try:
            tags_index = contains_tags.index(True)
        except ValueError:
            tags_index = len(content_list) - 1
        return content_list[:tags_index]

    def delete_banners(self, content_list):
        contains_banners = [
            True if '\n\t\t\t\t\t\t\t\t{{#en_desarrollo}}\n\t\t\t\t\t\t\t\t\t' in text else False
            for text in content_list
        ]
        try:
            banner_index = contains_banners.index(True)
        except ValueError:
            banner_index = len(content_list) - 1
        return content_list[:banner_index]
