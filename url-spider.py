import scrapy

from pydispatch import dispatcher
from scrapy import signals

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ToScrapeSpiderXPath(scrapy.Spider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    name = 'url-spider'
    start_urls = [
        'http://cai.rz.fh-ingolstadt.de/mediawiki/index.php/Computer_Science_and_Artificial_Intelligence',
    ]

    scrapedLinks = []

    def parse(self, response):
        for link in response.xpath('.//a/@href'):
            newUrl = str(link.get())
            if(self.testLinkInteresting(newUrl)):
                    if("http://cai.rz.fh-ingolstadt.de/" in newUrl):
                        absoluteUrl = newUrl
                    else:
                        absoluteUrl = "http://cai.rz.fh-ingolstadt.de/" + newUrl

                    if self.testNewLink(absoluteUrl):
                        self.scrapedLinks.append(absoluteUrl)
                        yield scrapy.Request(absoluteUrl, callback=self.parse)

    def spider_closed(self, spider):
        for i in self.scrapedLinks:
            print(i)

    def makeLinkComplete(self, url):
        if("http://cai.rz.fh-ingolstadt.de/" in url):
            return url
        else:
            return "http://cai.rz.fh-ingolstadt.de/" + url

    def testLinkInteresting(self, url):
        if("/mediawiki/index.php/" in url):
            if("/Special:" in url):
                return False
            if("/File:" in url):
                return False
            #if("/Category:" in url):
                #return False
            return True

    def testNewLink(self, url):
        if url in self.scrapedLinks:
            return False
        else:
            print(len(self.scrapedLinks))
            return True
