import hashlib

from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from .consts import CLOUDINARY_FOLDER_NAME
from .utils import get_url_from_cloudinary_storage


class Author(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(unidecode(self.name))
            unique_slug = original_slug
            num = 1

            while Author.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(unidecode(self.name))
            unique_slug = original_slug
            num = 1

            while Genre.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

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
    created_date = models.DateTimeField()
    status = models.CharField(
        max_length=9,
        choices=Status.choices,
        default=Status.ONGOING,
    )
    source = models.CharField(max_length=255, blank=True)
    cover_photo = CloudinaryField('image')
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=True)
    genres = models.ManyToManyField(Genre, through='StoryGenre')
    latest_chapter = models.ForeignKey('Chapter', related_name='latest_chapter', on_delete=models.SET_NULL, null=True,
                                       blank=True)

    def generate_cover_photo_public_id(self, original_url):
        hash_digest = hashlib.sha256(original_url.encode()).hexdigest()[:10]
        image_folder = f"{CLOUDINARY_FOLDER_NAME}/images"
        public_id = f"{image_folder}/{self.slug}-{hash_digest}"
        return public_id

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(unidecode(self.title))
            unique_slug = original_slug
            num = 1

            while Story.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{original_slug}-{num}'
                num += 1

            self.slug = unique_slug

        if isinstance(self.cover_photo, str) and self.cover_photo.startswith('http'):
            public_id = self.generate_cover_photo_public_id(self.cover_photo)
            image_url = get_url_from_cloudinary_storage(public_id)
            if image_url is None:
                upload_result = upload(
                    self.cover_photo,
                    public_id=public_id
                )
                self.cover_photo = upload_result.get('url')
            else:
                self.cover_photo = image_url
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
    published_date = models.DateTimeField()
    number_chapter = models.IntegerField(db_index=True)

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
