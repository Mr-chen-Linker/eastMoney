# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from eastMoney.items import FundinfoItem, StockItem


class EastmoneyPipeline(object):

    def __init__(self):
        self.filename = codecs.open("fund.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        if isinstance(item, FundinfoItem):
            self.write(item)
        elif isinstance(item, StockItem):
            self.write(item)
        return item

    def close_spider(self, spider):
        self.filename.close()

    def write(self, item):
        text = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(text)
