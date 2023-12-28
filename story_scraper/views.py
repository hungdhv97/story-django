from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render

from .forms import ListStoriesCrawlForm, SomeStoriesCrawlForm


def prepare_crawl_command(form, command_template):
    command_args = ' '.join([f'--{key.replace("_", "-")} {value}' for key, value in form.cleaned_data.items()])
    return command_template.format(command_args)


@staff_member_required
def crawl_list_stories_view(request):
    form = ListStoriesCrawlForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        command = prepare_crawl_command(form, 'python manage.py crawl_list_stories {}')
        return JsonResponse({"command": command})
    return render(request, 'crawl_stories.html', {'form': form, 'command': ''})


@staff_member_required
def crawl_some_stories_view(request):
    form = SomeStoriesCrawlForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        command = prepare_crawl_command(form, 'python manage.py crawl_some_stories {}')
        return JsonResponse({"command": command})
    return render(request, 'crawl_stories.html', {'form': form, 'command': ''})
