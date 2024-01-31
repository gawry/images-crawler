from scrapy import exceptions

from itemadapter import ItemAdapter
from images_crawler.services import DownloadLimiter
from images_crawler.db_manager import DatabaseManager


class DownloadLimiterPipeline:
    def __init__(self, max_downloads: int = 1000):
        self.limiter = DownloadLimiter(max_downloads)
    
    @classmethod
    def from_crawler(cls, crawler):
        MAX_DOWNLOADS = crawler.settings.attributes["MAX_DOWNLOADS"].value
        return  cls(max_downloads=MAX_DOWNLOADS)
        
    def process_item(self, item, spider):
        if self.limiter.is_limit_reached():
            raise exceptions.CloseSpider(f'More than {self.limiter.downloads} items were downloaded the spider was suspended to avoid banning')
        self.limiter.increment()
        return item



class SQLAlchemyPipeline:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    @classmethod
    def from_crawler(cls, crawler):
        db_uri = crawler.settings.get('DATABASE_URL')
        db_manager = DatabaseManager(db_uri)
        return cls(db_manager)

    def process_item(self, item, spider):
        for image_data in item['images']:
            self.db_manager.add_image({
                'url': image_data['url'],
                'file_hash': image_data['checksum'],
                'path': image_data['path']
            })
        return item

    def close_spider(self, spider):
        self.db_manager.dispose()