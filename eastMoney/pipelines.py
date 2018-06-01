# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from eastMoney.items import FundinfoItem, StockItem
import pymysql


class EastmoneyPipeline(object):

    def __init__(self):
        self.db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="eastmoney",
                                  charset="utf8")
        self.cur = self.db.cursor()
        self.cur.execute("select version();")
        version = self.cur.fetchone()
        print("DB version IS :" + str(version))

    def process_item(self, item, spider):

        if isinstance(item, FundinfoItem):
            print("开始向mysql数据库中写入tfundinfo数据")
            # 插入数据
            _insert_sql = "insert into tfundinfo (fund_code,fund_name,fundinfo_url,fundmarket_date,fund_nav,fund_cav,fundnavrate_1day,fundnavrate_1week,fundnavrate_1month,fundnavrate_3month,fundnavrate_6month,fund_cost) \
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            _insert_data = (
                item["fund_code"], item["fund_name"], item["fundinfo_url"], item["fundmarket_date"], item["fund_nav"],
                item["fund_cav"], item["fundnavrate_1day"], item["fundnavrate_1week"], item["fundnavrate_1month"],
                item["fundnavrate_3month"], item["fundnavrate_6month"], item["fund_cost"])
            try:

                # 执行语句方法，入参有2个：第一个是sql语句，第二个是需要传入的值，类型可以是列表或元祖
                self.cur.execute(_insert_sql, _insert_data)

            except Exception:
                self.db.rollback()
                print("都插入失败了")
            finally:
                self.db.commit()
        elif isinstance(item, StockItem):
            print("开始向mysql数据库中写入tstockinfo数据")
            _insert_sql = "insert into tstockinfo (fundcode,stock_code,stock_name,accounted_of_nav,holding_num,worth_sum,lastdate) \
                        values (%s,%s,%s,%s,%s,%s,%s)"""

            _insert_data = (
                item["fundcode"], item["stock_code"], item["stock_name"], item["accounted_of_nav"], item["holding_num"],
                item["worth_sum"], item["lastdate"])
            try:
                # 执行语句方法，入参有2个：第一个是sql语句，第二个是需要传入的值，类型可以是列表或元祖
                self.cur.execute(_insert_sql, _insert_data)

            except Exception:
                self.db.rollback()
                print("都插入失败了")
            finally:
                self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
