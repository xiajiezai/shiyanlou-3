# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, User, engine
from scrapy.exceptions import DropItem
from datetime import datetime
from shiyanlou.items import CourseItem

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        #use different process mothods for different item types
        if isinstance(item, CourseItem):
            self._process_course_item(item)
        else:
            self._process_user_item(item)
        return item    

    def _process_course_item(self, item):
        #send parsed items here and perfome the steps below
        #if type of parsed item does match that in models.py, then process
        item['students']=int(item['students'])
        if item['students']<1000:
            raise DropItem('Students less than 1000.')
        else:
            self.session.add(Course(**item))
            #item是字典，把整个字典传给course函数，函数的返回值作为session.add的参数
            #星号变量的特殊用法http://python.jobbole.com/86589/
        return item

    def _process_user_item(self, item):
        item['level']=int(item['level'][1:])
        #change L26 into 26
        item['join_date']=datetime.strptime(item['join_date'].split()[0],'%Y-%m-%d').date()
        #convert '2017-01-01 joined shiyanlou' into a date object
        item['learn_course_num']=int(item['learn_course_num'])
        self.session.add(User(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session=Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
