import scrapy

from story_scraper.story_scraper.spiders.story_handler import StoryHandler


class SomeStoriesSpider(scrapy.Spider):
    name = 'some_stories_spider'
    allowed_domains = ['truyenfull.vn']
    custom_settings = {
        'ITEM_PIPELINES': {
            "story_scraper.story_scraper.pipelines.ClearDatabasePipeline": 300,
        }
    }

    def __init__(self, story_urls, *args, **kwargs):
        super(SomeStoriesSpider, self).__init__(*args, **kwargs)
        self.start_urls = story_urls.split(',') if story_urls else []
        self.story_handler = StoryHandler()

    def parse(self, response):
        yield from self.story_handler.parse_story(response)
