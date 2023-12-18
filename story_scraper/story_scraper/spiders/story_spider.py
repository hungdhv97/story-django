import re
from datetime import datetime

import scrapy

from stories.models import Author, Genre, Story, Status, StoryGenre, Chapter
from story_scraper.story_scraper.const import MAX_PAGES_STORIES, MAX_PAGES_CHAPTERS


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
        self.current_page_story = 0

    def parse(self, response):
        story_urls = response.css('.col-truyen-main .list-truyen .row h3 a::attr(href)').getall()

        for story_url in story_urls:
            yield response.follow(story_url, callback=self.parse_story)

        next_page = response.xpath(
            '//div[contains(@class, "pagination")]//li[contains(@class, "active")]/following-sibling::'
            'li[1][not(contains(@class, "dropup"))]/a/@href').get()

        self.current_page_story += 1
        if next_page is not None and self.current_page_story < MAX_PAGES_STORIES:
            yield response.follow(next_page, callback=self.parse)

    def parse_story(self, response):
        genres = self.save_genres(response)
        author = self.save_author(response)
        story = self.save_story(response, author)
        self.save_story_genres(story, genres)
        yield from self.save_chapters(response, story, 1)

    def save_genres(self, response):
        list_genres = []
        genres = response.css('.col-truyen-main .info-holder .info a[itemprop="genre"]::text').getall()
        for genre in genres:
            existing_genre = Genre.objects.filter(name=genre.strip()).first()
            if existing_genre is not None:
                list_genres.append(existing_genre)
            else:
                genre = Genre(name=genre)
                genre.save()
                list_genres.append(genre)
        return list_genres

    def save_author(self, response):
        author_name = response.css('.col-truyen-main .info-holder .info a[itemprop="author"]::text').get()
        existing_author = Author.objects.filter(name=author_name.replace('\u200B', '').strip()).first()
        if existing_author is not None:
            return existing_author
        author = Author(name=author_name)
        author.save()
        return author

    def save_story(self, response, author):
        title = response.css('.col-truyen-main h3.title::text').get()
        description = re.sub(
            r'<[^>]+>',
            '',
            re.sub(
                r'<br\s*/?>',
                '\n',
                response.css('.col-truyen-main .desc-text').get())
        ).replace("\u00A0", " ")
        created_date = datetime.now().strftime("%Y-%m-%d")
        # Mapping of conditions to statuses
        status_ongoing = response.css('.col-truyen-main .info-holder .info span.text-primary::text').get()
        status_success = response.css('.col-truyen-main .info-holder .info span.text-success::text').get()
        status_conditions = {
            Status.ONGOING: status_ongoing is not None,
            Status.COMPLETED: status_success is not None,
        }
        # Find the first true condition and set the status, default to DROPPED
        status = next((status for status, condition in status_conditions.items() if condition), Status.DROPPED)
        story_source = response.css('.col-truyen-main .info-holder .info span.source::text').get()
        source = story_source or ""
        cover_photo = response.css('.col-truyen-main .info-holder img::attr(src)').get()

        existing_story = Story.objects.filter(slug="slug").first()
        if existing_story is not None:
            return existing_story
        story = Story(title=title, description=description, author_id=author.id, created_date=created_date,
                      status=status,
                      source=source, cover_photo=cover_photo)
        story.save()
        return story

    def save_story_genres(self, story, genres):
        for genre in genres:
            StoryGenre(story_id=story.id, genre_id=genre.id).save()

    def save_chapters(self, response, story, page_chapter):
        if page_chapter > MAX_PAGES_CHAPTERS:
            return
        chapter_urls = response.css('.col-truyen-main #list-chapter .row ul li a::attr(href)').getall()

        for chapter_url in chapter_urls:
            yield response.follow(chapter_url, callback=self.save_chapter, cb_kwargs={'story': story})

        next_page = response.xpath(
            '//ul[contains(@class, "pagination")]//li[contains(@class, "active")]/following-sibling::'
            'li[1][not(contains(@class, "dropup"))]/a/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.save_chapters,
                                  cb_kwargs={'story': story, 'page_chapter': page_chapter + 1})

    def save_chapter(self, response, story):
        title = response.css(".chapter-title::text").get()
        content = "\n".join(response.css(".chapter-c::text").getall())
        published_date = datetime.now().strftime("%Y-%m-%d")

        existing_chapter = Chapter.objects.filter(story_id=story.id, title=title).first()
        if existing_chapter is None:
            chapter = Chapter(story_id=story.id, title=title, content=content,
                              published_date=published_date)
            chapter.save()
