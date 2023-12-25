from django.urls import path

from .views import crawl_stories_view

urlpatterns = [
    path('crawl-stories/', crawl_stories_view, name='crawl-stories'),
]
