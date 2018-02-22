# -*- coding: utf-8 -*-
import scrapy

class LoginSpider(scrapy.Spider):
	name='login_spider'

	start_urls=['https://www.shiyanlou.com/login']

	def parse(self,response):
		#fill in forms on login page
		csrf_token=response.xpath('//div[@class="login-body"]//input[@id="csrf_token"]/@value').extract_first()
		self.logger.info(csrf_token)
		return scrapy.FormRequest.from_response(
			response,
			formdata={
				'csrf_token':csrf_token,
				'login':'example@xx.com',
				'password':'xxxxxx'
			},
			callback=self.after_login
		)

	def after_login(self,response):
		# return an iterable of Requests (you can return a list of requests or write a generator function) which the Spider will begin to crawl from.
		return[scrapy.Request(
			url='https://www.shiyanlou.com/user/332855/',
			callback=self.parse_after_login
			)]		

	def parse_after_login(self,response):
		#In the callback function, you parse the response (web page) and return either dicts with extracted data
		return{
			'experiment_count':response.xpath('(//span[@class="info-text"])[2]/text()').re_first('[^\d]*(\d*)[^\d]*'),
			'experiment_time':response.xpath('(//span[@class="info-text"])[3]/text()').re_first('[^\d]*(\d*)[^\d]*')
		}
