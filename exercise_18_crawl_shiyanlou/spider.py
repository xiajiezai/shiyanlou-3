import scrapy
class syl_course_spider(scrapy.Spider):
	name='course'
	
	@property
	def start_urls(self):
		url_tmpl='https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
		return (url_tmpl.format(i) for i in range(1,23))

	#a crude way of doing this
	'''
	def start_requests(self):
		url_tmpl='https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
		urls=(url_tmpl.format(i) for i in range(1,23))
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
	'''
	def parse(self,response):
		for course in response.css('div.course-body'):
			yield{
			'name':course.css('div.course-name::text').extract_first(),
			'description':course.css('div.course-desc::text').extract_first(),
			'type':course.css('div.course-footer span.course-money pull-right::text').extract_first(),
			'students':course.xpath('.//span[contains(@class,"pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
			#you can only use double quotes here
			}