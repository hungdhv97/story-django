from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from story_scraper.story_scraper.spiders.genre_spider import GenreSpider

from story_scraper.story_scraper import settings


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(GenreSpider)
        process.start()
