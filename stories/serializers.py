from rest_framework import serializers
from .models import Author, Genre, Story, Chapter, Rating, StoryGenre


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = serializers.SerializerMethodField()
    latestChapter = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'

    def get_genre(self, obj):
        return GenreSerializer(obj.storygenre_set.all(), many=True).data

    def get_latest_chapter(self, obj):
        latest_chapter = Chapter.objects.filter(story=obj).order_by('-chapter_number').first()
        return ChapterSerializer(latest_chapter).data


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
