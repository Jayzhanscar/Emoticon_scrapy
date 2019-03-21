# -*- coding: utf-8 -*-
import scrapy
from tutoial.items import ImgItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['doutula.com']
    start_urls = ['https://www.doutula.com/photo/list/']
    # 调度计数器
    count = 1
    
    def parse(self, response):
        QuotesSpider.count += 1
        content = response.css('a')
        for con in content:
            get_data = con.xpath('//img')
            for data in get_data:
                if data.css('::attr(data-original)').extract_first():
                    item = ImgItem()
                    item['title'] = data.css('::attr(alt)').extract_first()
                    item['path'] = data.css('::attr(data-original)').extract_first()
                    yield item
        
        # next = response.css('li').xpath('//a').css('.page-link::attr(href)').extract_first()
        
        url = 'https://www.doutula.com/photo/list/?page=' + str(QuotesSpider.count)
        # yield scrap.Request(url=url, callback=self.parse)
        if QuotesSpider.count < 10:
            yield scrapy.Request(url=url, callback=self.parse)
        else:
            return 'end'
