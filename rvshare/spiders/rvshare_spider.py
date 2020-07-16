from scrapy import Spider, Request
from rvshare.items import RvshareItem
import re

class RvshareSpider(Spider):
    name = 'rvshare_spider'
    allowed_urls = ['https://rvshare.com/']
    start_urls = ['https://rvshare.com/rv-rental?location=New%20York%2C%20NY%2C%20USA&lat=40.7127753&lng=-74.0059728']

    def parse(self, response):
        # city_urls = response.xpath('//ul[@class="popular-destinations__list"]/li/a/@href').extract()[:-1]
        # for url in city_urls:
        #     yield Request(url=url, callback=self.)


        num_pages = response.xpath('//div[@class="Box-mhcuhk-0 Text-pe2fh5-0 ghgJjM"]/text()').extract()
        num_pages = int(int(re.findall('of (\d+)',num_pages[0])[0])/27)

        url_list = [f'https://rvshare.com/rv-rental?location=New%20York%2C%20NY%2C%20USA&lat=40.7127753&lng=-74.0059728&page={i}' for i in range(num_pages)]
        for url in url_list:
            yield Request(url=url, callback=self.parse_results_page)

    def parse_results_page(self, response):
        listing_urls = response.xpath('//div[@class="Box-mhcuhk-0 Flex-ofb2h0-0 RVCardstyles__MetaWrapper-sc-1bwuzqm-5 hCxFSr"]/a/@href').extract()
        listing_urls = [f'https://rvshare.com/{suffix}' for suffix in listing_urls]
        
        for url in listing_urls:
            yield Request(url=url, callback=self.parse_listing_page)

    def parse_listing_page(self, response):
        name = response.xpath('//div[@class="RvTitle__RvTitleContainer-hskm81-0 ecAmPT"]/div/h1/text()').extract_first()
        price = response.xpath('//div[@data-id="nightly-rate"]/span/text()').extract_first()
        
        summary = response.xpath('//div[@class="styles__SummaryItem-sc-1ylo37q-1 ddrTmu"]/text()').extract()
        
        location = summary[0]
        sleeps = int(re.findall('Sleeps (\d+)', summary[1])[0])
        year = int(summary[2])
        vehicle_type = summary[3]
        length = summary[4]

        item = RvshareItem()
        item['name'] = name
        item['price'] = price
        item['location'] = location
        item['sleeps'] = sleeps
        item['year'] = year
        item['vehicle_type'] = vehicle_type
        item['length'] = length

        yield item
        
