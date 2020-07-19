from scrapy import Spider, Request
from rvshare.items import RvshareItem
import re

class RvshareSpider(Spider):
    name = 'rvshare_spider'
    allowed_urls = ['https://rvshare.com/']
    start_urls = ['https://rvshare.com/']

    def parse(self, response):
        city_urls = response.xpath('//ul[@class="popular-destinations__list"]')[1].xpath('./li[@class="popular-destinations__list-item"]/a/@href').extract()[:-1]
        # print(city_urls)
        for url in city_urls[:5]:
            yield Request(url=url, callback=self.parse_city_listings)

    def parse_city_listings(self, response):
        num_pages = response.xpath('//div[@class="Box-mhcuhk-0 Text-pe2fh5-0 ghgJjM"]/text()').extract()
        num_pages = int(int(re.findall('of (\d+)',num_pages[0])[0])/27)
        initial_url = response.request.url
        # print('='*50)
        # print(num_pages)

        url_list = [f'{initial_url}?page={i}' for i in range(1, num_pages+1)]
        for url in url_list[:5]:
            yield Request(url=url, callback=self.parse_results_page)

    def parse_results_page(self, response):
        listing_urls = response.xpath('//div[@class="Box-mhcuhk-0 Flex-ofb2h0-0 RVCardstyles__MetaWrapper-sc-1bwuzqm-5 hCxFSr"]/a/@href').extract()
        listing_urls = [f'https://rvshare.com/{suffix}' for suffix in listing_urls]
        distance_list = response.xpath('//div[@class="Box-mhcuhk-0 Flex-ofb2h0-0 lfwVrU"]/div/span/span/text()').extract()
        # print(distance_list)
        
        for i, url in enumerate(listing_urls[:5]):
            yield Request(url=url, callback=self.parse_listing_page, meta={'distance': distance_list[i][:]})

    def parse_listing_page(self, response):
        name = response.xpath('//div[@class="RvTitle__RvTitleContainer-hskm81-0 ecAmPT"]/div/h1/text()').extract_first()
        # price = response.xpath('//div[@data-id="nightly-rate"]/span/text()').extract_first()
        price_nightly = response.xpath('//*[@id="rates"]/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/text()').extract_first()
        price_weekly = response.xpath('//*[@id="rates"]/div[2]/div/div[1]/div[2]/div[2]/div/div[1]/text()').extract_first()
        price_monthly = response.xpath('//*[@id="rates"]/div[2]/div/div[1]/div[2]/div[3]/div/div[1]/text()').extract_first()
        summary = response.xpath('//div[@class="styles__SummaryItem-sc-1ylo37q-1 ddrTmu"]/text()').extract()
        
        location = summary[0]
        sleeps = int(re.findall('Sleeps (\d+)', summary[1])[0])
        year = int(summary[2])
        vehicle_type = summary[3]
        length = summary[4]

        distance = response.meta['distance']

        rv_details = response.xpath('//div[@data-id="rv-details"]/ul/li/span/text()').extract()
        kitchen = response.xpath('//div[@data-id="kitchen-amenities"]/ul/li/span/text()').extract()
        bathroom = response.xpath('//div[@data-id="bathroom-amenities"]/ul/li/span/text()').extract()
        temperature_control = response.xpath('//div[@data-id="temperature-amenities"]/ul/li/span/text()').extract()
        entertainment = response.xpath('//div[@data-id="entertainment-amenities"]/ul/li/span/text()').extract()
        cancellation = response.xpath('//div[@class="CancellationPolicy__Container-sc-1vbh5ca-0 jSIiWW"]/div/text()').extract_first()
        cancellation = re.findall('- (\D+)', cancellation)[0]

        item = RvshareItem()
        item['name'] = name
        item['price_nightly'] = price_nightly
        item['price_weekly'] = price_weekly
        item['price_monthly'] = price_monthly
        item['location'] = location
        item['sleeps'] = sleeps
        item['year'] = year
        item['vehicle_type'] = vehicle_type
        item['length'] = length
        item['distance'] = distance
        item['rv_details'] = rv_details
        item['kitchen'] = kitchen
        item['bathroom'] = bathroom
        item['temperature_control'] = temperature_control
        item['entertainment'] = entertainment
        item['cancellation'] = cancellation
        

        yield item
        
