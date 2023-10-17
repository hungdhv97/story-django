from datetime import datetime, timedelta

from django.db import models
from rest_framework import serializers

from .models import Story, Author, Genre, Chapter, StoryGenre, ReadingStats, Rating


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_number', 'publish_date']


class StorySerializer(serializers.ModelSerializer):
    total_chapters = serializers.IntegerField()
    # total_reads = serializers.IntegerField()
    total_reads_2 = serializers.IntegerField()
    is_new = serializers.BooleanField()
    # is_hot = serializers.SerializerMethodField()
    # rating = serializers.SerializerMethodField()
    # genres = serializers.SerializerMethodField()
    # latest_chapter = serializers.SerializerMethodField()
    author = AuthorSerializer()

    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'author',
            # 'genres',
            'total_chapters',
            # 'total_reads',
            'total_reads_2',
            'created_date', 'status', 'source',
            'cover_photo',
            'is_new',
            # 'is_hot', 'rating',
            'slug',
            # 'latest_chapter'
        ]

    # def get_total_chapters(self, obj):
    #     return Chapter.objects.filter(story=obj).count()
    #
    # def get_total_reads(self, obj):
    #     total_reads = ReadingStats.objects.filter(story=obj).aggregate(models.Sum('read_count'))['read_count__sum']
    #     return total_reads if total_reads else 0
    #
    # def get_is_new(self, obj):
    #     return (datetime.now().date() - obj.created_date) <= timedelta(days=30)
    #
    # def get_is_hot(self, obj):
    #     total_reads = ReadingStats.objects.filter(story=obj).aggregate(models.Sum('read_count'))['read_count__sum']
    #     return total_reads >= 500 if total_reads else False
    #
    # def get_rating(self, obj):
    #     ratings = Rating.objects.filter(story=obj)
    #     rating_sum = ratings.aggregate(models.Sum('rating_value'))['rating_value__sum']
    #     rating_count = ratings.count()
    #     return rating_sum / rating_count if rating_count > 0 else 0
    #
    # def get_genres(self, obj):
    #     story_genres = StoryGenre.objects.filter(story=obj)
    #     genres = Genre.objects.filter(storygenre__in=story_genres)
    #     return GenreSerializer(genres, many=True).data
    #
    # def get_latest_chapter(self, obj):
    #     latest_chapter = Chapter.objects.filter(story=obj).order_by('-chapter_number').first()
    #     return ChapterDetailSerializer(latest_chapter).data if latest_chapter else None


class StoryQueryParameterSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=False)
    genre_id = serializers.IntegerField(required=False)
    slug = serializers.CharField(required=False)
    is_hot = serializers.BooleanField(required=False)
    is_new = serializers.BooleanField(required=False)
    is_completed = serializers.BooleanField(required=False)