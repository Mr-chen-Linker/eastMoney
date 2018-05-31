# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EastmoneyItem(scrapy.Item):

    # 列表页的基金代码
    fundcode=scrapy.Field()
    # 列表页的基金名称
    fundname=scrapy.Field()
    # 基金详情页链接
    fundinfourl=scrapy.Field()

    # 基金前十大持仓股信息
    stockname_in_fund=scrapy.Field()
    # 持仓占比
    stockaccounted_in_fund=scrapy.Field()
    # 涨跌幅
    stockrange_in_fund=scrapy.Field()
    # # 前十持仓占比合计
    # sumstocketaccounted_in_fund=scrapy.Field()
    # # 持仓信息截止日期
    # lastdate=scrapy.Field()