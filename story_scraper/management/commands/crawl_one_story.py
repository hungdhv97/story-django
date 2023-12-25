from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from story_scraper.story_scraper import settings as my_settings
from story_scraper.story_scraper.spiders.one_story_spider import OneStorySpider


class Command(BaseCommand):
    help = 'Crawl specific stories based on provided URLs'

    def add_arguments(self, parser):
        parser.add_argument('story_urls', type=str, help='Comma-separated list of story URLs')

    def handle(self, *args, **options):
        story_urls = options['story_urls']

        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(OneStorySpider, story_urls=story_urls)
        process.start()
