# -*- coding: utf-8 -*-
import scrapy
from github_crawl_ch.items import GithubCrawlChItem

class GithubcrawlSpider(scrapy.Spider):
	name = 'githubcrawl'

	@property
	def start_urls(self):
		url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
		return (url_tmpl.format(i) for i in range(1,5))

	def parse(self, response):
		for repos in response.css('li.py-4'):
			item=GithubCrawlChItem()
			item['name']=repos.xpath('.//a[contains(@itemprop,"codeRe")]/text()').re_first('\s*(.+)')
			item['update_time']=repos.xpath('.//relative-time/@datetime').extract_first()
			course_url=response.urljoin(repos.xpath('.//div[@class="d-inline-block mb-1"]/h3/a/@href').extract_first())
			request=scrapy.Request(course_url,callback=self.parse_on_page)
			request.meta['item']=item
			yield request

	def parse_on_page(self,response):
		item=response.meta['item']
		item['commits']=response.xpath('.//span[@class="num text-emphasized"]/text()')[0].re_first('\s*(\d)*\s')
		item['branches']=response.xpath('.//span[@class="num text-emphasized"]/text()')[1].re_first('\s*(\d)*\s')
		item['releases']=response.xpath('.//span[@class="num text-emphasized"]/text()')[2].re_first('\s*(\d)*\s')
		yield item