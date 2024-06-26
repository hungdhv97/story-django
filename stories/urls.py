from django.urls import path

from .views import (
    AuthorDetailView,
    ChapterDetailView,
    ChapterListView,
    ChapterShortInfoListView,
    GenreDetailView,
    GenreListView,
    IncreaseReadCount,
    RatingCreateView,
    StoryDetailView,
    StoryListView,
    StorySearchView,
    TopStoryListView,
)

urlpatterns = [
    path('stories/', StoryListView.as_view(), name='story-list'),
    path('stories/<slug:slug>/', StoryDetailView.as_view(), name='story-detail'),
    path('stories/<slug:slug>/chapters/', ChapterListView.as_view(), name='chapter-list'),
    path('top/stories/', TopStoryListView.as_view(), name='top-story-list'),
    path(
        'stories/<slug:slug>/chapters/short-info/', ChapterShortInfoListView.as_view(),
        name='chapter-short-info-list'
    ),
    path('chapters/<int:chapter_id>/', ChapterDetailView.as_view(), name='chapter-detail'),
    path('authors/<int:author_id>/', AuthorDetailView.as_view(), name='author-detail'),
    path('ratings/create/', RatingCreateView.as_view(), name='rating-create'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<slug:slug>/', GenreDetailView.as_view(), name='genre-detail'),
    path('search/', StorySearchView.as_view(), name='story-search'),
    path('increase-read-count/<int:story_id>/', IncreaseReadCount.as_view(), name='increase-read-count'),
]
