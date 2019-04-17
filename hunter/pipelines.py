# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import logging
from scrapy.utils.project import project_data_dir
from hunter.middlewares import SqliteHandle


class HunterPipeline(object):
    def process_item(self, item, spider):
        return item


class CwlPipline(object):
    def process_item(self, item, spider):
        datadir = '/'.join(project_data_dir().split('/')[:-1]) + '/data'
        try:
            os.makedirs(datadir)
        except OSError:
            pass

        # 创建数据库文件
        dbfile = '{}/{}.sqlite'.format(datadir, spider.name)
        SH = SqliteHandle(dbfile)
        SH.create_table(spider.name, self.table_model())
        try:
            SH.insert(spider.name, item)
            logging.info('Current records and storage success')
        except Exception as e:
            logging.warning(e)
        SH.close()
        return item


    def table_model(self):
        """Double chromosphere data table model"""
        columns = []
        columns.append('id integer primary key autoincrement')
        columns.append('code integer unique not null')
        columns.append('date varchar(10) not null')
        columns.append('red text not null')
        columns.append('blue text not null')
        columns.append('sales integer')
        columns.append('pool_money integer')
        columns.append('note integer')
        return columns


class LotteryPipline(object):
    def process_item(self, item, spider):
        datadir = '/'.join(project_data_dir().split('/')[:-1]) + '/data'
        try:
            os.makedirs(datadir)
        except OSError:
            pass

        dbfile = '{}/{}.sqlite'.format(datadir, spider.name)
        SH = SqliteHandle(dbfile)
        SH.create_table(spider.name, self.table_model())
        try:
            SH.insert(spider.name, item)
            logging.info('Current records and storage success')
        except Exception as e:
            logging.warning(e)
        SH.close()
        return item


    def table_model(self):
        """Big lottery data table model"""
        columns = list()
        columns.append('id integer  primary key autoincrement')
        columns.append('phase_number integer unique not null')
        columns.append('note_number integer')
        columns.append('bonus integer not null')
        columns.append('red_number text not null')
        columns.append('blue_number text not null')
        return columns
