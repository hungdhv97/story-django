# story-django

## Setup

* Tạo environment
    ```shell
    python -m venv venv 
    pip install -r requirements.txt 
    ```
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
        * Tạo pipeline clear database
* Viết spider
    * Tạo spider để crawl dữ liệu
    * Lưu Dữ liệu vào Django Database:
        * Trong phương thức `parse` của spider, bạn sẽ tạo các instance của `DjangoItem` và điền dữ liệu vào đó, sau đó
          trả lại các item này và `save()`.
    * Chạy scrapy
        * Chạy spider
      ```shell
      scrapy crawl story_spider
      ```
* Cấu hình **Django Project (story_site)**  trong file `settings.py` dự án **Scrapy**

```python
import os
import sys
import django

sys.path.append('/home/sotatek/study/story-django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'story_site.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
```

* Cấu hình app **Scrapy (story_scraper)** trong file `settings.py` của dự án **Django Project (story_site)**

```python
INSTALLED_APPS = [
    ...,
    'story_scraper'
]
```

* Thêm **Django Command** run spider
    * Tạo file management/commands/crawl.py trong project **Scrapy (story_scraper)**
      ```shell
      python manage.py crawl
      ```
    