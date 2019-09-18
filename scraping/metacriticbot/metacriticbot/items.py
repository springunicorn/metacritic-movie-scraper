# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

USER_AGENT = "Mozilla/5.0 (X11; Linux i686; rv:24.0) "\
           + "Gecko/20140903 Firefox/24.0 Iceweasel/24.8.0"


class Movie(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # General info
    name = scrapy.Field()
    link = scrapy.Field()
    datePublished = scrapy.Field()
    director = scrapy.Field()
    publisher = scrapy.Field()
    actor = scrapy.Field()
    maturity_rating = scrapy.Field()
    genre = scrapy.Field()
    metascore = scrapy.Field()
    critics_reviews_count = scrapy.Field()
    user_score = scrapy.Field()
    user_reviews_count = scrapy.Field()
    description = scrapy.Field()


class Summary(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    summary = scrapy.Field()
