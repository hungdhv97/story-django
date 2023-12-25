from django.contrib import messages
from django.core.management import call_command
from django.shortcuts import render, redirect

from .forms import StoryCrawlForm


def crawl_stories_view(request):
    if request.method == 'POST':
        form = StoryCrawlForm(request.POST)
        if form.is_valid():
            from_story_index = form.cleaned_data['from_story_index']
            to_story_index = form.cleaned_data['to_story_index']
            from_chapter_index = form.cleaned_data['from_chapter_index']
            to_chapter_index = form.cleaned_data['to_chapter_index']

            try:
                # Run the command
                call_command('crawl_list_stories',
                             from_story_index=from_story_index,
                             to_story_index=to_story_index,
                             from_chapter_index=from_chapter_index,
                             to_chapter_index=to_chapter_index)

                messages.success(request, 'Stories crawl initiated successfully.')
            except Exception as e:
                messages.error(request, f'Error occurred: {e}')

            # Redirect to the same page or another success page
            return redirect('crawl-stories')
    else:
        form = StoryCrawlForm()

    return render(request, 'crawl_stories.html', {'form': form})
