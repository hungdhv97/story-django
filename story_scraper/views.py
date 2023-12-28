from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .forms import ListStoriesCrawlForm, SomeStoriesCrawlForm


@staff_member_required
def crawl_list_stories_view(request):
    form = ListStoriesCrawlForm()
    return render(request, 'crawl_stories.html', {'form': form})


@staff_member_required
def crawl_some_stories_view(request):
    form = SomeStoriesCrawlForm()
    return render(request, 'crawl_stories.html', {'form': form})
