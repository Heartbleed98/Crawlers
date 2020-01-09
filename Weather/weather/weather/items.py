# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AirItem(scrapy.Item):
    city = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    air = scrapy.Field()