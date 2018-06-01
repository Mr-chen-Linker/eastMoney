# -*- coding: utf-8 -*-
import scrapy
import json
from eastMoney.items import FundinfoItem, StockItem
from scrapy.utils.project import get_project_settings


class FundmarketSpider(scrapy.Spider):
    name = 'fundrank'
    allowed_domains = ['fund.eastmoney.com']

    # settings = get_project_settings()
    #
    # FUND_STOCK_LASE_YERA = settings.get("FUND_STOCK_LASE_YERA")
    # FUND_TRADE_STATUS = settings.get("FUND_TRADE_STATUS")


    offset = 1
    url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&gs=0&sc=zzf&st=desc&sd=2017-05-30&ed=2018-05-30&pn=50&dx=0&pi="

    start_urls = [url + str(offset)]

    def parse(self, response):
        # bytys转为str
        data = response.body.decode("utf-8")
        # 截取基金列表信息
        data = data[data.find('['):data.find(']') + 1]
        fundslist = json.loads(data)

        fundcode_lists = []
        for fund in fundslist:
            # 至此，得到了一个基金信息，都是list类型
            fundinfo = fund.split(',')
            item = FundinfoItem()

            # 基金代码
            item["fund_code"] = fundinfo[0]
            # 基金名称
            item["fund_name"] = fundinfo[1]
            # 基金详情页链接
            item["fundinfo_url"] = "http://fund.eastmoney.com/" + str(fundinfo[0]) + ".html"
            # 行情日期
            item["fundmarket_date"] = fundinfo[3]
            # 基金的单位净值
            item["fund_nav"] = fundinfo[4]
            # 基金的累计净值
            item["fund_cav"] = fundinfo[5]
            # 基金净值涨跌幅-日
            item["fundnavrate_1day"] = fundinfo[6]
            # 基金净值涨跌幅-周
            item["fundnavrate_1week"] = fundinfo[7]
            # 基金净值涨跌幅-1月
            item["fundnavrate_1month"] = fundinfo[8]
            # 基金净值涨跌幅-3月
            item["fundnavrate_3month"] = fundinfo[9]
            # 基金净值涨跌幅-6月
            item["fundnavrate_6month"] = fundinfo[10]
            # 基金的手续费
            item["fund_cost"] = fundinfo[-5]

            yield item

            fundcode_lists.append(fundinfo[0])

        if self.offset <= 50:
            self.offset += 1
            yield scrapy.Request(url=self.url + str(self.offset), callback=self.parse)

        # 生成基金前十大持仓信息请求
        for fundcode in fundcode_lists:
            url = "http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&topline=10&year=2018&code=" + str(
                fundcode)
            yield scrapy.Request(url, callback=self.parse_stock, meta={"fundcode": fundcode})

    def parse_stock(self, response):

        # 为了与基金代码关联
        fundcode = response.meta["fundcode"]

        # 获取持仓截止日期
        dates = response.xpath("//label/font/text()").extract()
        # 按每个季度分开遍历
        # print("季度数量为" + str(len(dates)))
        for i in range(1, len(dates) + 1):
            # 得到其中一个季度的根节点
            # print("i为-----------" + str(i))
            node = response.xpath("//div[@class='box'][" + str(i) + "]")

            fundnum = node.xpath(".//tbody/tr").extract()
            # print("每季度的基金数量" + str(len(fundnum)))
            for j in range(1, len(fundnum) + 1):
                item = StockItem()

                # print("j为------------" + str(j))
                # 一个季度的前10个股票信息
                tr = node.xpath(".//tbody/tr[" + str(j) + "]")

                # 股票代码
                item["stock_code"] = tr.xpath("./td[2]/a/text() | ./td[2]/span/text()").extract_first(
                    default="not-found")
                # 股票名称
                item["stock_name"] = tr.xpath("./td[3]/a/text()").extract_first(default="not-found")

                # 该股票净值占比
                item["accounted_of_nav"] = tr.xpath("./td[last()-2]/text()").extract_first(default="not-found")
                # 持股数（单位：万股
                item["holding_num"] = tr.xpath("./td[last()-1]/text()").extract_first(default="not-found")
                # 持仓市值（单位：万元）
                item["worth_sum"] = tr.xpath("./td[last()]/text()").extract_first(default="not-found")
                # 持仓截止日期
                item["lastdate"] = dates[i - 1]
                # 基金代码
                item["fundcode"] = fundcode

                yield item
