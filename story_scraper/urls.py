from django.urls import path

from .views import crawl_list_stories_view, crawl_some_stories_view

urlpatterns = [
    path('crawl-list-stories/', crawl_list_stories_view, name='crawl-list-stories'),
    path('crawl-some-stories/', crawl_some_stories_view, name='crawl-some-stories'),
]
