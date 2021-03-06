import scrapy
class github_spider(scrapy.Spider):
	name='github'
	
	@property
	def start_urls(self):
		url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
		return (url_tmpl.format(i) for i in range(1,5))

	def parse(self,response):
		for repos in response.css('li.py-4'):
			yield{
			'name':repos.xpath('.//a[contains(@itemprop,"codeRe")]/text()').re_first('\s*(.+)'),
			'update_time':repos.xpath('.//relative-time/@datetime').extract_first()
			}