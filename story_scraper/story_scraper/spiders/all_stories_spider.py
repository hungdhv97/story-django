import scrapy

from story_scraper.story_scraper.consts import MAX_PAGES_STORIES
from story_scraper.story_scraper.spiders.story_handler import StoryHandler


class AllStoriesSpider(scrapy.Spider):
    name = 'all_story_spider'
    allowed_domains = ['truyenfull.vn']
    start_urls = ['https://truyenfull.vn/danh-sach/truyen-hot/']

    custom_settings = {
        'ITEM_PIPELINES': {
            "story_scraper.story_scraper.pipelines.ClearDatabasePipeline": 300,
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.story_handler = StoryHandler()

    def parse(self, response):
        page_number = response.meta.get('page_number', 1)
        story_urls = response.css('.col-truyen-main .list-truyen .row h3 a::attr(href)').getall()

        for story_url in story_urls:
            yield response.follow(story_url, callback=self.story_handler.parse_story)

        next_page = response.xpath(
            '//div[contains(@class, "pagination")]//li[contains(@class, "active")]/following-sibling::'
            'li[1][not(contains(@class, "dropup"))]/a/@href').get()

        if next_page is not None and page_number < MAX_PAGES_STORIES:
            yield response.follow(next_page, callback=self.parse, meta={'page_number': page_number + 1})
