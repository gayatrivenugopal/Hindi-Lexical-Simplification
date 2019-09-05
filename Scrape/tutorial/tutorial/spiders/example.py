# -*- coding: utf-8 -*-
import scrapy
from build_corpus import clean_text

class ExampleSpider(scrapy.Spider):
    name = 'example'
    #allowed_domains = ['example.com']
    start_urls = ['http://premchand.co.in/story/patni-se-pati']

    def parse(self, response):
        #page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'w', encoding = 'utf-8') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        filename = response.url[response.url.rfind('/')+1:]+'.txt'
        file = open(filename , 'w', encoding = 'utf-8')
        content = ''.join(response.xpath('//body//p//text()').extract())
        content = content.replace('।', ' .')
        file.write(content)
        file.close()
        clean_text('/opt/PhD/Work/JHWNL_1_2/Code/Scrape/tutorial', [filename])
#TODO: upload on github, save no. of lines in url and no. of lines in file and compare (for additional lines in file)
