import scrapy

from stories.models import Author, Genre
from story_scraper.story_scraper.const import MAX_PAGES


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
        self.save_genre(response)
        self.save_author(response)
        self.save_story(response)

    def save_genre(self, response):
        genres = response.css('.col-truyen-main .info-holder .info a[itemprop="genre"]::text').getall()
        for genre in genres:
            existing_genre = Genre.objects.filter(name=genre.strip()).first()
            if existing_genre is None:
                Genre(name=genre).save()

    def save_author(self, response):
        author_name = response.css('.col-truyen-main .info-holder .info a[itemprop="author"]::text').get()
        existing_author = Author.objects.filter(name=author_name.replace('\u200B', '').strip()).first()
        if existing_author is None:
            Author(name=author_name).save()

    # def save_story(self, response):
    #     story_item = Story()
    #
    #     # Extract story details
    #     story_item['title'] = response.css('.story-title::text').get().strip()
    #     story_item['description'] = response.css('.story-description::text').get().strip()
    #
    #     # Extract author
    #     author_name = response.css('.author-name::text').get().strip()
    #     author = Author.objects.filter(name=author_name).first()
    #     story_item['author'] = author
    #
    #     # Extract and associate genres
    #     genre_names = response.css('.genre-list .genre::text').getall()
    #     genres = [Genre.objects.filter(name=gn.strip()).first() for gn in genre_names]
    #     story_item['genres'] = genres
    #
    #     # Save the story item
    #     story_item.save()
