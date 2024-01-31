import json

import scrapy
import pytest

from scrapy.http import HtmlResponse, TextResponse
from scrapy.utils.test import get_crawler
from scrapy.utils.project import get_project_settings
from images_crawler.spiders.freeimages import FreeImagesSpider
from scrapy.selector import SelectorList, Selector


from images_crawler.items import ImageItem


from scrapy.utils.reactor import install_reactor
install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')


def test_parse_search_results():
    crawler = get_crawler(FreeImagesSpider, settings_dict=get_project_settings())
    spider = FreeImagesSpider(keyword='dogs')
    crawler.crawl(spider)
    response = HtmlResponse(url='https://www.freeimages.com/search/dogs')
    def mock_css(selector):
        if selector == '.grid-link:not(.istock-a-tag)::attr(href)':
            
            mock_html1 = '<a class="grid-link" href="/photo/image1"></div>'
            mock_html2 = '<a class="grid-link" href="/photo/image2"></div>'
            mock_html3 = '<a class="grid-link" href="/photo/image3"></div>'
            return SelectorList([scrapy.Selector(text=mock_html1).css('.grid-link:not(.istock-a-tag)::attr(href)'), 
                                 scrapy.Selector(text=mock_html2).css('.grid-link:not(.istock-a-tag)::attr(href)'), 
                                 scrapy.Selector(text=mock_html3).css('.grid-link:not(.istock-a-tag)::attr(href)')])
        if selector == '#btn-see-more::attr(href)' or selector =='.next-page-link::attr(href)':
            return SelectorList([scrapy.Selector(text='/search/dogs/2')])
    response.css = mock_css

    results = list(spider.parse_search_results(response))

    assert (len(results) == 4)
    assert (results[0].url == 'https://www.freeimages.com/download/image1')
    assert (results[1].url == 'https://www.freeimages.com/download/image2')
    assert (results[2].url == 'https://www.freeimages.com/download/image3')
    crawler.stop()

def test_parse_download_page():
    crawler = get_crawler(FreeImagesSpider, settings_dict=get_project_settings())
    spider = FreeImagesSpider(keyword='dogs')
    crawler.crawl(spider)
    response = HtmlResponse(url='https://www.freeimages.com/download/image1')

    def mock_css(selector):
        if selector == '#direct-download::attr(data-hash)':
            mock_html = '<div id="direct-download" data-hash="hash1"></div>'
            return SelectorList([Selector(text=mock_html).css('#direct-download::attr(data-hash)')])
        elif selector == '#direct-download::attr(data-image-id)':
            mock_html = '<div id="direct-download" data-image-id="id1"></div>'
            return SelectorList([Selector(text=mock_html).css('#direct-download::attr(data-image-id)')])

    response.css = mock_css

    results = list(spider.parse_download_page(response))
    print(results)
    print(results[0].body)

    assert (len(results) == 1)
    assert (results[0].method == 'POST')
    assert (results[0].url == 'https://www.freeimages.com/ajax/download')
    assert (results[0].body == b'{"id": "id1", "hash": "hash1"}')
    crawler.stop()

def test_parse_search_results():
    crawler = get_crawler(FreeImagesSpider, settings_dict=get_project_settings())
    spider = FreeImagesSpider(keyword='dogs')
    crawler.crawl(spider)
    response = HtmlResponse(url='https://www.freeimages.com/search/dogs')
    def mock_css(selector):
        if selector == '.grid-link:not(.istock-a-tag)::attr(href)':
            
            mock_html1 = '<a class="grid-link" href="/photo/image1"></div>'
            mock_html2 = '<a class="grid-link" href="/photo/image2"></div>'
            mock_html3 = '<a class="grid-link" href="/photo/image3"></div>'
            return SelectorList([scrapy.Selector(text=mock_html1).css('.grid-link:not(.istock-a-tag)::attr(href)'), 
                                 scrapy.Selector(text=mock_html2).css('.grid-link:not(.istock-a-tag)::attr(href)'), 
                                 scrapy.Selector(text=mock_html3).css('.grid-link:not(.istock-a-tag)::attr(href)')])
        if selector == '#btn-see-more::attr(href)' or selector =='.next-page-link::attr(href)':
            return SelectorList([scrapy.Selector(text='/search/dogs/2')])
    response.css = mock_css

    results = list(spider.parse_search_results(response))

    assert (len(results) == 4)
    assert (results[0].url == 'https://www.freeimages.com/download/image1')
    assert (results[1].url == 'https://www.freeimages.com/download/image2')
    assert (results[2].url == 'https://www.freeimages.com/download/image3')
    crawler.stop()

def test_parse_download_page():
    crawler = get_crawler(FreeImagesSpider, settings_dict=get_project_settings())
    spider = FreeImagesSpider(keyword='dogs')
    crawler.crawl(spider)
    response = HtmlResponse(url='https://www.freeimages.com/download/image1')

    def mock_css(selector):
        if selector == '#direct-download::attr(data-hash)':
            mock_html = '<div id="direct-download" data-hash="hash1"></div>'
            return SelectorList([Selector(text=mock_html).css('#direct-download::attr(data-hash)')])
        elif selector == '#direct-download::attr(data-image-id)':
            mock_html = '<div id="direct-download" data-image-id="id1"></div>'
            return SelectorList([Selector(text=mock_html).css('#direct-download::attr(data-image-id)')])

    response.css = mock_css

    results = list(spider.parse_download_page(response))
    print(results)
    print(results[0].body)

    assert (len(results) == 1)
    assert (results[0].method == 'POST')
    assert (results[0].url == 'https://www.freeimages.com/ajax/download')
    assert (results[0].body == b'{"id": "id1", "hash": "hash1"}')
    crawler.stop()
    
def test_download_image():
    spider = FreeImagesSpider()
    response = scrapy.http.HtmlResponse(url='https://www.freeimages.com/download/image1', body=b'{"error": false, "data": {"url": "https://www.example.com/image1.jpg"}}')
    results = list(spider.download_image(response))
    assert (len(results) == 1)
    assert (isinstance(results[0], ImageItem))
    assert (results[0]["image_urls"] == ['https://www.example.com/image1.jpg'])