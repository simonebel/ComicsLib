# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorsItem(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    nick_name = scrapy.Field()
    activity = scrapy.Field()
    biography = scrapy.Field()


class SeriesItem(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    nick_name = scrapy.Field()
    activity = scrapy.Field()
    biography = scrapy.Field()
