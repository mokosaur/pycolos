import requests
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
