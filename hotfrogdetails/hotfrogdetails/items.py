# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotfrogdetailsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website_name = scrapy.Field()
    website_link = scrapy.Field()
    phone = scrapy.Field()
    business_info = scrapy.Field()
    business_description = scrapy.Field()
    direction = scrapy.Field()
    find = scrapy.Field()
    near = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()

