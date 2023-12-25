from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from story_scraper.story_scraper import settings
from story_scraper.story_scraper.spiders.list_stories_spider import ListStoriesSpider


class Command(BaseCommand):
    help = 'Crawl list of stories'

    def add_arguments(self, parser):
        parser.add_argument('from_story_index', type=int, help='from story index')
        parser.add_argument('to_story_index', type=int, help='to story index')
        parser.add_argument('from_chapter_index', type=int, help='from chapter index')
        parser.add_argument('to_chapter_index', type=int, help='to chapter index')

    def handle(self, *args, **options):
        from_story_index = options['from_story_index']
        to_story_index = options['to_story_index']
        from_chapter_index = options['from_chapter_index']
        to_chapter_index = options['to_chapter_index']

        crawler_settings = Settings()
        crawler_settings.setmodule(settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(
            ListStoriesSpider,
            from_story_index=from_story_index,
            to_story_index=to_story_index,
            from_chapter_index=from_chapter_index,
            to_chapter_index=to_chapter_index
        )
        process.start()
