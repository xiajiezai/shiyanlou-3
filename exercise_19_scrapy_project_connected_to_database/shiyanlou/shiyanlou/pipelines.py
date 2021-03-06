# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, engine
from scrapy.exceptions import DropItem

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        #send parsed items here and perfome the steps below
        item['students']=int(item['students'])
        if item['students']<1000:
        	raise DropItem('Students less than 1000.')
        else:
        	self.session.add(Course(**item))
        return item

    def open_spider(self, spider):
    	Session = sessionmaker(bind=engine)
    	self.session=Session()

    def close_spider(self, spider):
    	self.session.commit()
    	self.session.close()
