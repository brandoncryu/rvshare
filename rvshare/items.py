# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RvshareItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    sleeps = scrapy.Field()
    year = scrapy.Field()
    vehicle_type = scrapy.Field()
    length = scrapy.Field()
    distance = scrapy.Field()

    

