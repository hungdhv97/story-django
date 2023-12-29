from django.urls import path

from .views import crawl_list_stories_view, crawl_some_stories_view

urlpatterns = [
    path('crawlliststories', crawl_list_stories_view, name='crawl-list-stories'),
    path('crawlsomestories', crawl_some_stories_view, name='crawl-some-stories'),
]
