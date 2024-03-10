import os
import re
import sys

import django

sys.path.append('/home/sotatek/study/story-django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'story_site.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from stories.models import Chapter


def extract_chapter_numbers():
    for chapter in Chapter.objects.all():
        print(chapter.id)
        try:
            match = re.search(r'Chương (\d+)', chapter.title)
            if match:
                number = int(match.group(1))
                chapter.number_chapter = number
            else:
                chapter.number_chapter = None
        except (ValueError, IndexError):
            chapter.number_chapter = None
        chapter.save()


extract_chapter_numbers()
