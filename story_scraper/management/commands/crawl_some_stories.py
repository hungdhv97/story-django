from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from story_scraper.story_scraper import settings as my_settings
from story_scraper.story_scraper.spiders.some_stories_spider import SomeStoriesSpider


class Command(BaseCommand):
    help = 'Crawl specific stories based on provided URLs'

    def add_arguments(self, parser):
        parser.add_argument('--story-urls', type=str, help='Comma-separated list of story URLs')
        parser.add_argument('--from_chapter_index', type=int, default=1, help='from chapter index')
        parser.add_argument('--to_chapter_index', type=int, default=20, help='to chapter index')

    def handle(self, *args, **options):
        story_urls = options['story_urls']
        from_chapter_index = options['from_chapter_index']
        to_chapter_index = options['to_chapter_index']

        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(
            SomeStoriesSpider,
            story_urls=story_urls,
            from_chapter_index=from_chapter_index,
            to_chapter_index=to_chapter_index
        )
        process.start()
