import scrapy

from stories.models import Author, Genre
from story_scraper.story_scraper.const import MAX_PAGES
from story_scraper.story_scraper.items import AuthorItem, GenreItem


class StorySpider(scrapy.Spider):
    name = 'story_spider'
    allowed_domains = ['truyenfull.vn']
    start_urls = ['https://truyenfull.vn/danh-sach/truyen-hot/']

    custom_settings = {
        'ITEM_PIPELINES': {
            "story_scraper.story_scraper.pipelines.ClearDatabasePipeline": 300,
        }
    }

    def __init__(self):
        self.current_page = 0

    def parse(self, response):
        story_urls = response.css('.col-truyen-main .list-truyen .row h3 a::attr(href)').getall()

        for story_url in story_urls:
            yield response.follow(story_url, callback=self.parse_story)

        next_page = response.xpath(
            '//div[contains(@class, "pagination")]//li[contains(@class, "active")]/following-sibling::'
            'li[1][not(contains(@class, "dropup"))]/a/@href').get()

        self.current_page += 1
        if next_page is not None and self.current_page < MAX_PAGES:
            yield response.follow(next_page, callback=self.parse)

    def parse_story(self, response):
        self.parse_genre(response)
        self.parse_author(response)

    def parse_genre(self, response):
        genres = response.css('.col-truyen-main .info-holder .info a[itemprop="genre"]::text').getall()
        for genre in genres:
            genre_item = GenreItem()
            genre_item['name'] = genre.strip()
            existing_author = Genre.objects.filter(name=genre_item['name']).first()
            if existing_author is None:
                genre_item.save()

    def parse_author(self, response):
        author_item = AuthorItem()
        author_name = response.css('.col-truyen-main .info-holder .info a[itemprop="author"]::text').get()
        author_item['name'] = author_name.replace('\u200B', '').strip()
        existing_author = Author.objects.filter(name=author_item['name']).first()
        if existing_author is None:
            author_item.save()
