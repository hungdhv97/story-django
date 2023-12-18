from django.contrib import admin
from django.utils.html import format_html

from .models import Author, Genre, Story, StoryGenre, Chapter, Rating, ReadingStats


class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_cover_photo', 'description', 'author_id', 'created_date',
                    'status', 'source', 'slug')

    def display_cover_photo(self, obj):
        if obj.cover_photo and hasattr(obj.cover_photo, 'url'):
            return format_html(
                '<img src="{}" width="100" />',
                obj.cover_photo.url,
            )
        return "No cover photo"

    display_cover_photo.short_description = 'Cover Photo'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StoryGenreAdmin(admin.ModelAdmin):
    list_display = ('story_id', 'genre_id')


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'story_id', 'title', 'content', 'published_date')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'story_id', 'rating_value')


class ReadingStatsAdmin(admin.ModelAdmin):
    list_display = ('story_id', 'read_count', 'date')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(StoryGenre, StoryGenreAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(ReadingStats, ReadingStatsAdmin)
