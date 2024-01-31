import scrapy
import json

from images_crawler.items import ImageItem

from scrapy.utils.reactor import install_reactor

class FreeImagesSpider(scrapy.Spider):
    name = 'freeimages'
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    
    def __init__(self, keyword='dogs', *args, **kwargs):
        super(FreeImagesSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.base_url = 'https://www.freeimages.com'
        self.current_page = 1
        self.start_urls = [f'{self.base_url}/search/{keyword}']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        # Extract image links
        for href in response.css('.grid-link:not(.istock-a-tag)::attr(href)').getall():
            image_slug = href.split('/')[-1]
            download_url = f'{self.base_url}/download/{image_slug}'
            yield scrapy.Request(url=download_url, callback=self.parse_download_page)

        # Handle pagination
        next_page = response.css('#btn-see-more::attr(href)').get() or response.css('.next-page-link::attr(href)').get()
        if next_page:
            self.current_page += 1
            yield response.follow(next_page, self.parse_search_results)

    def parse_download_page(self, response):
        # Extract details for POST request
        data_hash = response.css('#direct-download::attr(data-hash)').get()
        image_id = response.css('#direct-download::attr(data-image-id)').get()

        # Make POST request for downloading
        post_url = f'{self.base_url}/ajax/download'
        data = {'id': image_id, 'hash': data_hash}
        yield scrapy.Request(url=post_url, method='POST', body=json.dumps(data), callback=self.download_image)

    def download_image(self, response):
        # Extract the redirect URL for the actual image
        image_data = json.loads(response.body)

        # Check if the URL is valid
        if not image_data.get("error", False):
            image_urls=[image_data.get("data", {}).get("url", "")]
            yield ImageItem(image_urls=image_urls)