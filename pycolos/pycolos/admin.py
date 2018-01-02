from django.contrib import admin

# Register your models here.
from markdownx.admin import MarkdownxModelAdmin

from pycolos.pycolos.models import Test, Question, Answer, TestSession, UserAnswer

admin.site.register(Test)
admin.site.register(Question, MarkdownxModelAdmin)
admin.site.register(Answer)
admin.site.register(TestSession)
admin.site.register(UserAnswer)