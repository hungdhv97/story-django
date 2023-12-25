from django import forms


class ListStoriesCrawlForm(forms.Form):
    from_story_index = forms.IntegerField(initial=1, min_value=1, label='From Story Index')
    to_story_index = forms.IntegerField(initial=10, min_value=1, label='To Story Index')
    from_chapter_index = forms.IntegerField(initial=1, min_value=1, label='From Chapter Index')
    to_chapter_index = forms.IntegerField(initial=20, min_value=1, label='To Chapter Index')


class SomeStoriesCrawlForm(forms.Form):
    story_urls = forms.CharField(widget=forms.Textarea, help_text='Enter comma-separated list of story URLs')
    from_chapter_index = forms.IntegerField(initial=1, min_value=1, label='From Chapter Index')
    to_chapter_index = forms.IntegerField(initial=20, min_value=1, label='To Chapter Index')
