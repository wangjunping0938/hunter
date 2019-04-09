# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from hunter.items import LotteryItem


class Headers(object):
    headers = {}
    headers['Accept'] = 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    headers['Cache-Control'] = 'max-age=0'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = 'www.lottery.gov.cn'
    headers['Upgrade-Insecure-Requests'] = 1


class Rules(object):
    parse = {}
    parse['block'] = '//div[@class="result"]/table/tbody//tr'
    parse['red_number'] = '//td[@class="red"]/text()'
    parse['blue_number'] = '//td[@class="blue"]/text()'
    parse['phase_number'] = '//td[1]/text()'
    parse['note_number'] = '//td[9]/text()'
    parse['bonus'] = '//td[10]/text()'


class LotterySpider(scrapy.Spider):
    name = 'lottery'
    allowed_domains = ['lottery.gov.cn']
    start_url = 'http://www.lottery.gov.cn/historykj/history.jspx?page=false&_ltype=dlt&termNum=100&startTerm=&endTerm='
    custom_settings = {'ITEM_PIPELINES':{'hunter.pipelines.LotteryPipline': 100}}

    def start_requests(self):
        yield Request(self.start_url, headers=Headers().headers, callback=self.parse)

    def parse(self, response):
        rules = Rules().parse
        block = response.xpath(rules['block']).extract()
        for b in block:
            item = LotteryItem()
            red_number = Selector(text=b).xpath(rules['red_number']).extract()
            blue_number = Selector(text=b).xpath(rules['blue_number']).extract()
            phase_number = Selector(text=b).xpath(rules['phase_number']).extract_first()
            note_number = Selector(text=b).xpath(rules['note_number']).extract_first()
            bonus = Selector(text=b).xpath(rules['bonus']).extract_first()

            item['red_number'] = ','.join(map(str, map(int, red_number)))
            item['blue_number'] = ','.join(map(str, map(int, blue_number)))
            item['phase_number'] = int(phase_number)
            item['note_number'] = int(note_number)
            item['bonus'] = int(float(bonus.replace(',', '')))
            yield item
