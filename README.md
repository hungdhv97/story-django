# story-django

## Setup

* Tạo và thiết lập **Project Django**
    * Tạo Project Django
      ```shell 
      django-admin startproject story_site
      ```
    * Tạo **Django App**
      ```shell
      python manage.py startapp stories
      ```
    * Thiết lập Database
        * Cấu hình trong file `settings.py` của project Django
    * Tạo mô hình **Django**
        * Định nghĩa mô hình: Trong file `models.py`
            * Author
            * Genre
            * Story
            * StoryGenre
            * Chapter
            * Rating
            * ReadingStats
        * Migrations
          ```shell
          python manage.py makemigrations
          ```
          ```shell
          python manage.py migrate
          ```

## Scrapy

* Thiết lập Scrapy
    * Tạo Project Scrapy
  ```shell
  scrapy startproject story_scraper
  ```
    * Cài đặt pipelines
        * Thiết lập pipeline sử dụng `DjangoItem` trong file `settings.py`
* Sử dụng DjangoItem
    * Tạo DjangoItem trong file `items.py` và định nghĩa các trường trong DjangoItem tương ứng với các fields trong
      Django models
* Viết spider
    * Tạo spider để crawl dữ liệu
    * Lưu Dữ liệu vào Django Database:
        * Trong phương thức `parse` của spider, bạn sẽ tạo các instance của `DjangoItem` và điền dữ liệu vào đó, sau đó
          trả lại các item này và `save()`.
    * Chạy scrapy
        * Chạy spider
      ```shell
      scrapy crawl spider_story
      ```

Cài đặt Pipelines: Trong settings.py của Scrapy, thiết lập pipeline để sử dụng DjangoItem.

* Cấu hình **Django** trong dự án **Scrapy**

```python
import os
import sys
import django

sys.path.append('/home/sotatek/study/story-django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'story_site.settings'
django.setup()
```

* Tạo **DjangoItem**

```python
from scrapy_djangoitem import DjangoItem

from stories.models import Genre


class GenreItem(DjangoItem):
    django_model = Genre
```

* Tạo **spider**

```python

```

* Lưu dữ liệu
    * **JSON**
      ```shell
      scrapy crawl spider_story -O stories.json
      ```
    * **CSV**
      ```shell
      scrapy crawl spider_story -O stories.csv
      ```
    * Đã settings
      ```shell
      scrapy crawl spider_story
      ```
    