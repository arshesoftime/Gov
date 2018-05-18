# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class GovItem(Item):
    title = Field()
    detail_url = Field()
    department = Field()
    res_date = Field()
    reply = Field()
    raise_date = Field()
    suggestion = Field()
