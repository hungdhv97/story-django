import requests
from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Author(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Status(models.TextChoices):
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    DROPPED = 'dropped', 'Dropped'


class Story(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_date = models.DateField()
    status = models.CharField(
        max_length=9,
        choices=Status.choices,
        default=Status.ONGOING,
    )
    source = models.CharField(max_length=255, blank=True)
    cover_photo = CloudinaryField('image')
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        original_slug = slugify(unidecode(self.title))
        unique_slug = original_slug
        num = 1

        while Story.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{original_slug}-{num}'
            num += 1

        self.slug = unique_slug

        if self.cover_photo and self.cover_photo.startswith('http'):
            image_url = self.cover_photo
            response = requests.get(image_url)
            if response.status_code == 200:
                upload_result = upload(response.content)
                self.cover_photo = upload_result.get('url')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class StoryGenre(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('story', 'genre'),)
        indexes = [
            models.Index(fields=['story', 'genre'], name='story_genre_idx'),
        ]


class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    published_date = models.DateField()

    def __str__(self):
        return f'{self.title}'


class Rating(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    rating_value = models.IntegerField()


class ReadingStats(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    read_count = models.IntegerField()
    date = models.DateField()

    class Meta:
        unique_together = (('story', 'date'),)
        indexes = [
            models.Index(fields=['story', 'date'], name='reading_stats_idx'),
        ]
