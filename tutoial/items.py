# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class TutoialItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     text = scrapy.Field()
#     author = scrapy.Field()
#     tags = scrapy.Field()


class ImgItem(scrapy.Item):
    """ 保存表情包文件地址 """
    title = scrapy.Field()
    path = scrapy.Field()
