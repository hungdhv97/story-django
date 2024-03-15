from django.contrib import admin
from django.urls import path

from story_scraper.models import CrawlListStories, CrawlSomeStories
from story_scraper.views import crawl_list_stories_view, crawl_some_stories_view


class CrawlListStoriesAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(crawl_list_stories_view)),
        ]
        return custom_urls + urls

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CrawlSomeStoriesAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(crawl_some_stories_view)),
        ]
        return custom_urls + urls

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(CrawlListStories, CrawlListStoriesAdmin)
admin.site.register(CrawlSomeStories, CrawlSomeStoriesAdmin)
