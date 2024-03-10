from datetime import timedelta
from math import ceil

from django.db.models import Sum, Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from .consts import NEW_STORY_DIFF_DATE, HOT_STORY_TOTAL_READS
from .models import Story, Author, Genre, Chapter, StoryGenre, Rating


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class ChapterInStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'number_chapter', 'title', 'published_date']


class StorySerializer(serializers.ModelSerializer):
    total_chapters = serializers.SerializerMethodField()
    total_reads = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_hot = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    latest_chapter = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    author = AuthorSerializer()

    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'author', 'genres', 'total_chapters', 'total_reads', 'created_date', 'status',
            'source', 'cover_photo', 'is_new', 'is_hot', 'avg_rating', 'slug', 'latest_chapter'
        ]

    def get_total_chapters(self, story):
        return story.chapter_set.count()

    def get_is_new(self, story):
        created_date = timezone.localtime(story.created_date)
        diff_days_ago = timezone.now() - timedelta(days=NEW_STORY_DIFF_DATE)
        return created_date >= diff_days_ago

    def get_cover_photo(self, story):
        return story.cover_photo.url

    def get_genres(self, story):
        story_genres = StoryGenre.objects.filter(story=story)
        genres = Genre.objects.filter(storygenre__in=story_genres)
        return GenreSerializer(genres, many=True).data

    def get_latest_chapter(self, story):
        latest_chapter = Chapter.objects.filter(story=story).order_by('-number_chapter').first()
        return ChapterInStorySerializer(latest_chapter).data if latest_chapter else None

    def get_total_reads(self, story):
        return story.readingstats_set.aggregate(Sum('read_count'))['read_count__sum'] or 0

    def get_is_hot(self, story):
        one_week_ago = timezone.now() - timedelta(days=7)
        total_reads_week = story.readingstats_set.filter(date__gte=one_week_ago).aggregate(Sum('read_count'))[
            'read_count__sum']
        return total_reads_week >= HOT_STORY_TOTAL_READS if total_reads_week is not None else False

    def get_avg_rating(self, story):
        return ceil(story.rating_set.aggregate(avg_rating=Avg('rating_value'))['avg_rating'] or 0)


class TopStorySerializer(serializers.ModelSerializer):
    total_reads = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ('id', 'title', 'cover_photo', 'slug', 'total_reads')

    def get_total_reads(self, story):
        return getattr(story, 'total_reads', 0)

    def get_cover_photo(self, story):
        return story.cover_photo.url if story.cover_photo else None


class StoryQueryParameterSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=False)
    genre_slug = serializers.CharField(required=False)
    is_hot = serializers.BooleanField(required=False)
    is_new = serializers.BooleanField(required=False)
    status = serializers.CharField(required=False)
    total_chapters_from = serializers.IntegerField(required=False)
    total_chapters_to = serializers.IntegerField(required=False)


class StoryInChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'slug']


class ChapterSerializer(serializers.ModelSerializer):
    story = StoryInChapterSerializer()

    class Meta:
        model = Chapter
        fields = ['id', 'story', 'number_chapter', 'title', 'content', 'published_date']


class RatingSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = Rating
        fields = ['slug', 'rating_value']

    def create(self, validated_data):
        slug = validated_data.pop('slug')
        story = get_object_or_404(Story, slug=slug)
        rating = Rating.objects.create(story=story, **validated_data)
        return rating

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['slug'] = instance.story.slug
        return representation
