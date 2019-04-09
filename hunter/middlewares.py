# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sqlite3
from selenium import webdriver
from scrapy import signals


class Browser(object):

    @staticmethod
    def firefox(user_agent):
        # Firefox browser simulation
        args = ['--ignore-ssl-errors=true']
        exec_path = re.sub(r'\n', '', os.popen('which geckodriver').read())
        firefox = webdriver.Firefox(executable_path=exec_path,
                                    log_path='/dev/null')
        firefox.implicitly_wait(60)
        firefox.set_page_load_timeout(60)
        firefox.maximize_window()
        firefox.desired_capabilities.update({'user_agent':user_agent})
        return firefox


class SqliteHandle(object):

    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.curs = self.conn.cursor()

    def create_table(self, tablename, columns):
        column = ', '.join(columns)
        sql = 'create table if not exists %s (%s)' % (tablename, column)
        self.curs.execute(sql)
        self.conn.commit()
        return sql

    def insert(self, tablename, data):
        keys = ', '.join(data.keys())
        values = tuple(data.values())
        sql = 'insert into %s (%s) values %s' % (tablename, keys, values)
        self.curs.execute(sql)
        self.conn.commit()
        return sql

    def fetch_one(self, tablename, key, value):
        sql = 'select * from %s where %s = "%s"' % (tablename, key, value)
        self.curs.execute(sql)
        rst = self.curs.fetchall()
        return rst

    def fetch_all(self, tablename):
        sql = 'select * from {}'.format(tablename)
        self.curs.execute(sql)
        rst = self.curs.fetchall()
        return rst

    def update(self, tablename, key, skey, data):
        sql = 'update %s set %s = ? where %s = ?' % (tablename, key, skey)
        self.curs.execute(sql, data)
        self.conn.commit()
        return sql

    def close(self):
        self.curs.close()
        self.conn.close()


class HunterSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HunterDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
