# -*- coding: utf-8 -*-
import scrapy
from ..items import EastmoneyItem


# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule


class FundmarketSpider(scrapy.Spider):
    name = 'fundmarket'
    allowed_domains = ['1234567.com.cn']

    start_urls = ['c#os_0;isall_1;ft_;pt_1']

    def parse(self, response):
        items = []
        # 获取每页的所有基金信息
        funds = response.xpath("//div[@id='tableDiv']/table[@align='center']/tbody/tr")
        # 遍历 取出基金代码和基金名称，然后继续往下请求详细信息页面
        for each in funds:
            item = EastmoneyItem()
            item["fundcode"] = each.xpath("./td[@class='bg bzdm']/text()")[0].extract()
            item["fundname"] = each.xpath("./td[@class='tol']/nobr/a/@title")[0].extract()
            item["fundinfourl"] = "http://www.1234567.com.cn/" + each.xpath("./td[@class='tol']/nobr/a[1]/@href")[
                0].extract()

            items.append(item)

        for item in items:
            yield scrapy.Request(url=item["fundinfourl"], callback=self.parse_stock, meta={"meta_1": item})

    def parse_stock(self, response):
        # 保存上面保存的基金代码和基金名称信息
        meta_1 = response.meta["meta_1"]

        stockinfo_list = response.xpath(
            "//div[@class='wrapper'][10]//div[contains(@class,'fund_item quotationItem_DataTable')]/div[@class='bd']/ul/li[@class='position_shares']//tr")
        # 如果该基金没有持仓股票信息，空的会有2个空行，那就不遍历取了
        print(len(stockinfo_list))
        if len(stockinfo_list) > 2:
            for each in stockinfo_list:
                # 做一个标记：如果遍历到表头：股票名称	持仓占比	涨跌幅	相关资讯，暂无数据，2行 这样的数据就过滤掉 不遍历
                if_table_th=each.xpath("./th")
                if len(if_table_th) == 0 :
                    item = EastmoneyItem()

                    # 保存上一请求得到的基金代码、名称、链接新
                    item["fundcode"] = meta_1["fundcode"]
                    item["fundname"] = meta_1["fundname"]
                    item["fundinfourl"] = meta_1["fundinfourl"]

                    # 基金前10大持仓股票名称
                    item["stockname_in_fund"] = each.xpath("./td[1]/a/@title")[0].extract()
                    # 持仓占比
                    item["stockaccounted_in_fund"] = each.xpath("./td[2]/text()")[0].extract()
                    # 涨跌幅
                    item["stockrange_in_fund"] = each.xpath("./td[3]/span/text()")[0].extract()

                    # 前十大持仓占比
                    # item["sumstocketaccounted_in_fund"] = each.xpath("./td/a/@title").extract()
                    # 持仓截止日期
                    # item["lastdate"] = each.xpath("./td/a/@title").extract()

                    yield item

    # def get_stockname_in_fund(self, response):  #     pass  #  # def get_stockaccounted_in_fund(self, response):  #     pass  #  # def get_stockrange_in_fund(self, response):  #     pass  #  # def get_sumstocketaccounted_in_fund(self, response):  #     pass  #  # def get_lastdate(self, response):  #     pass
