# -*- coding: utf-8 -*-
import scrapy
from multi_page.items import MultiPageItem


class MultipageSpider(scrapy.Spider):
    name = 'multipage'
    # allowed_domains = ['shiyanlou.com/courses'] keep this line and you will get no results
    start_urls = ['https://shiyanlou.com/courses/']

    def parse(self, response):
        for course in response.css('a.course-box'):
            item=MultiPageItem()
            item['name']=course.xpath('.//img/@alt').extract()
            item['image']=course.xpath('.//img/@src').extract()
            course_url=response.urljoin(course.xpath('@href').extract_first())
            request=scrapy.Request(course_url,callback=self.parse_author)
            request.meta['item']=item
            yield request


    def parse_author(self, response):
        item=response.meta['item']
        item['author']=response.xpath('//div[@class="mooc-info"]/div[@class="name"]/strong/text()').extract_first()
        yield item


