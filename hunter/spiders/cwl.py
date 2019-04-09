# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.http import Request
from hunter.items import CwlItem


class Headers(object):
    headers = {}
    headers['Accept'] = 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    headers['Cache-Control'] = 'max-age=0'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = 'www.cwl.gov.cn'
    headers['Upgrade-Insecure-Requests'] = 1
    headers['Referer'] = 'http://www.cwl.gov.cn/kjxx/ssq/kjgg/'


class CwlSpider(scrapy.Spider):
    name = 'cwl'
    allowed_domains = ['www.cwl.gov.cn']
    start_url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=100'
    custom_settings = {'ITEM_PIPELINES':{'hunter.pipelines.CwlPipline': 100}}

    def start_requests(self):
        headers = Headers().headers
        yield Request(self.start_url, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body_as_unicode())['result']
        item = CwlItem()
        for d in data:
            item['code'] = int(d['code'])
            item['date'] = ''.join(re.compile(r'\d+').findall(d['date']))
            item['red'] = ','.join(map(str, map(int, d['red'].split(','))))
            item['blue'] = int(d['blue'])
            item['sales'] = int(d['sales'])
            item['pool_money'] = int(d['poolmoney'])
            item['note'] = int(d['prizegrades'][0]['typenum'])
            yield item
