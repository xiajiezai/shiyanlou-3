# -*- coding: utf-8 -*-
import scrapy
from courses_image.items import CoursesImageItem

class CoursesImageSpider(scrapy.Spider):
    name = 'courses_image'
    start_urls = ['https://shiyanlou.com/courses/']

    def parse(self, response):
        item=CoursesImageItem()
        item['image_urls']=response.xpath('//div[@class="course-img"]/img/@src').extract()
        print(item)
        yield item