# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RvshareItem(scrapy.Item):
    name = scrapy.Field()
    price_nightly = scrapy.Field()
    price_weekly = scrapy.Field()
    price_monthly = scrapy.Field()
    location = scrapy.Field()
    sleeps = scrapy.Field()
    year = scrapy.Field()
    vehicle_type = scrapy.Field()
    length = scrapy.Field()
    distance = scrapy.Field()
    rv_details = scrapy.Field()
    kitchen = scrapy.Field()
    bathroom =  scrapy.Field()
    temperature_control = scrapy.Field()
    entertainment = scrapy.Field()
    cancellation = scrapy.Field()

    

