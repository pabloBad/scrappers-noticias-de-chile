# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    author = scrapy.Field()
    author_link = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    tags_links = scrapy.Field()
    author_twitter = scrapy.Field()
    link = scrapy.Field()
    publication_date = scrapy.Field()
    publication_hour = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    content = scrapy.Field()
    embedded_links = scrapy.Field()
    tags = scrapy.Field()
