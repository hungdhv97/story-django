from rest_framework import serializers

from .models import Story, Author, Genre, Chapter, StoryGenre


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
    total_chapters = serializers.IntegerField(read_only=True)
    total_reads = serializers.IntegerField(read_only=True)
    is_new = serializers.BooleanField(read_only=True)
    is_hot = serializers.BooleanField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    genres = serializers.SerializerMethodField()
    latest_chapter = serializers.SerializerMethodField()
    author = AuthorSerializer()

    class Meta:
        model = Story
        fields = [
            'id', 'title', 'description', 'author', 'genres', 'total_chapters', 'total_reads', 'created_date', 'status',
            'source', 'cover_photo', 'is_new', 'is_hot', 'avg_rating', 'slug', 'latest_chapter'
        ]

    def get_genres(self, obj):
        story_genres = StoryGenre.objects.filter(story=obj)
        genres = Genre.objects.filter(storygenre__in=story_genres)
        return GenreSerializer(genres, many=True).data

    def get_latest_chapter(self, obj):
        latest_chapter = Chapter.objects.filter(story=obj).order_by('-chapter_number').first()
        return ChapterDetailSerializer(latest_chapter).data if latest_chapter else None


class StoryQueryParameterSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=False)
    genre_id = serializers.IntegerField(required=False)
    is_hot = serializers.BooleanField(required=False)
    is_new = serializers.BooleanField(required=False)
    status = serializers.CharField(required=False)
