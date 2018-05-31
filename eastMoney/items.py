# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundinfoItem(scrapy.Item):
    # 基金基本信息

    # 基金代码
    fund_code = scrapy.Field()
    # 列表页的基金名称
    fund_name = scrapy.Field()
    # 基金详情页链接
    fundinfo_url = scrapy.Field()
    # 行情日期
    fundmarket_date = scrapy.Field()
    # 基金的单位净值
    fund_nav = scrapy.Field()
    # 基金的累计净值
    fund_cav = scrapy.Field()
    # 基金净值涨跌幅-日
    fundnavrate_1day = scrapy.Field()
    # 基金净值涨跌幅-周
    fundnavrate_1week = scrapy.Field()
    # 基金净值涨跌幅-1月
    fundnavrate_1month = scrapy.Field()
    # 基金净值涨跌幅-3月
    fundnavrate_3month = scrapy.Field()
    # 基金净值涨跌幅-6月
    fundnavrate_6month = scrapy.Field()
    # 基金的手续费
    fund_cost = scrapy.Field()


class StockItem(scrapy.Item):
    # 前十大持仓股信息

    # 股票代码
    stock_code = scrapy.Field()
    # 股票名称
    stock_name = scrapy.Field()
    # 该股票净值占比
    accounted_of_nav = scrapy.Field()
    # 持股数（单位：万股）
    holding_num = scrapy.Field()
    # 持仓市值（单位：万元）
    worth_sum = scrapy.Field()
    # 持仓截止日期
    lastdate = scrapy.Field()
    # 基金代码
    fundcode = scrapy.Field()
