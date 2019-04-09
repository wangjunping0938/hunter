# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HunterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LotteryItem(scrapy.Item):
    # Big lotto crawl field settings
    red_number = scrapy.Field()  #红色号码
    blue_number = scrapy.Field()  #蓝色号码
    phase_number = scrapy.Field()  #期号
    note_number = scrapy.Field()  #注数
    bonus = scrapy.Field()  #奖金


class CwlItem(scrapy.Item):
    # Double chromosphere crawling field settings
    code = scrapy.Field()  #期号
    date = scrapy.Field()  #日期
    red = scrapy.Field()  #红色号码
    blue = scrapy.Field()  #蓝色号码
    sales = scrapy.Field()  #销售额
    pool_money = scrapy.Field()  #奖池金额
    note = scrapy.Field()  #一等奖注数
