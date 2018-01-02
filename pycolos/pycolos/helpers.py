import requests
from django import template
from django.template.defaulttags import register
from django.utils.safestring import mark_safe


class ProgressBar:
    def __init__(self, index, count):
        self.index = index + 1
        self.count = count
        self.progress = round((index + 1) /count * 100)


@mark_safe
def markdown_to_html(markdown):
    url = 'https://api.github.com/markdown'
    r = requests.post(url, json={"text": markdown})
    return r.content


@register.filter(is_safe=True)
def css_class(value):
    difficulty_to_colors = {
        'VE': 'success',
        'E': 'info',
        'M': 'primary',
        'H': 'warning',
        'VH': 'danger'
    }
    return 'btn-' + difficulty_to_colors[value]


@register.filter(is_safe=True)
def difficulty(value):
    difficulty = {
        'VE': 'Bardzo Łatwe',
        'E': 'Łatwe',
        'M': 'Średnie',
        'H': 'Trudne',
        'VH': 'Ekspert'
    }
    return difficulty[value]
