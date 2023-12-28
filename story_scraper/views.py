from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .forms import ListStoriesCrawlForm, SomeStoriesCrawlForm


@staff_member_required
def crawl_list_stories_view(request):
    form = ListStoriesCrawlForm()
    for field in form.fields.values():
        field.widget.attrs['class'] = ('shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 '
                                       'leading-tight focus:outline-none focus:shadow-outline')
    return render(request, 'crawl_stories.html', {'form': form})


@staff_member_required
def crawl_some_stories_view(request):
    form = SomeStoriesCrawlForm()
    for field in form.fields.values():
        field.widget.attrs['class'] = ('shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 '
                                       'leading-tight focus:outline-none focus:shadow-outline')
    return render(request, 'crawl_stories.html', {'form': form})
