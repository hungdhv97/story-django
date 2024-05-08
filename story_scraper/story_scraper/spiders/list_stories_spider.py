import math

from scrapy import (
    Request,
    Spider,
)

from story_scraper.story_scraper.spiders.story_handler import StoryHandler


class ListStoriesSpider(Spider):
    name = 'list_stories_spider'
    allowed_domains = ['truyenfull.vn']
    base_url = 'https://truyenfull.vn/danh-sach/truyen-hot/trang-{}'

    custom_settings = {
        'ITEM_PIPELINES': {
            "story_scraper.story_scraper.pipelines.ClearDatabasePipeline": 300,
        },
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def __init__(self, from_story_index, to_story_index, from_chapter_index, to_chapter_index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_story_index = from_story_index
        self.to_story_index = to_story_index
        self.story_handler = StoryHandler(from_chapter_index, to_chapter_index)
        self.stories_per_page = None

    def start_requests(self):
        yield Request(url=self.base_url.format(1), callback=self.parse_initial)

    def parse_initial(self, response):
        stories = response.css('.col-truyen-main .list-truyen .row h3 a::attr(href)')
        self.stories_per_page = len(stories)
        from_page = math.ceil(self.from_story_index / self.stories_per_page)
        yield Request(url=self.base_url.format(from_page), callback=self.parse)

    def parse(self, response):
        page_number = int(response.url.split('trang-')[-1].split('/')[0])
        start_index_on_page = (self.from_story_index - 1) % self.stories_per_page if page_number == math.ceil(
            self.from_story_index / self.stories_per_page
        ) else 0
        end_index_on_page = (self.to_story_index - 1) % self.stories_per_page if page_number == math.ceil(
            self.to_story_index / self.stories_per_page
        ) else (self.stories_per_page - 1)

        story_urls = response.css('.col-truyen-main .list-truyen .row h3 a::attr(href)').getall()
        for story_url in story_urls[start_index_on_page:end_index_on_page + 1]:
            yield response.follow(story_url, callback=self.story_handler.parse_story)

        if page_number * self.stories_per_page < self.to_story_index:
            yield Request(url=self.base_url.format(page_number + 1), callback=self.parse)
