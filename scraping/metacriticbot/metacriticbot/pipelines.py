# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy.xlib.pydispatch import dispatcher
# ^depricated, using PyDispatcher instead
from pydispatch import dispatcher
from scrapy import signals
import xlwt
from datetime import datetime
from scrapy.utils.project import get_project_settings
import os
from metacriticbot.items import Movie

settings = get_project_settings()

class MetacriticbotPipeline(object):
    def process_item(self, item, spider):
        #so that userscore resembles metascore 0..100 scale
        #some non-numeric values such as 'tbd' are left out
        #for the sake of uniformity
        # try:
        #     item['user_score'] = int(float(item['user_score'])*10)
        # except ValueError:
        #     item['user_score'] = 'NA'
        #convert to Year-month-day format
        # if item['datePublished'] != 'NA' and item['datePublished'] != 'TBA':
            # item['datePublished'] = datetime.strptime(item['datePublished'], '%B %d, %Y').strftime('%Y-%m-%d')
        #leave only N out of "N Ratings" for user ratings
        #item['user_reviews_count'] = item['user_reviews_count'].split()[2]
        return item

class XlsExportPipeline(object):


    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        #from_crawler(self.spider_opened, signals.spider_opened)
        #from_crawler(self.spider_closed, signals.spider_closed)
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet("Metacritic")
        self.row_number = 0

    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(MySpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_opened, signals.spider_opened)
    #     return spider
    #write header
    def spider_opened(self, spider):
        item = Movie()
        keys = item.fields.keys() #item.keys to get field names
        for index, key in enumerate(keys):
            self.sheet.write(self.row_number, index, key) # row, column, value

    def spider_closed(self, spider):
        timestr = settings.get('TIMESTR')
        relpath = settings.get('RELPATH')
        xls_fname = os.path.join(relpath, 'data', "metacritic-" + timestr + ".xls")
        self.workbook.save(xls_fname)

    def process_item(self, item, spider):
        self.row_number = self.row_number + 1
        values = item.values()
        for index, val in enumerate(values):
            self.sheet.write(self.row_number, index, val) # row, column, value
        return item
