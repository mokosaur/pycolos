from django.contrib import admin

# Register your models here.
from markdownx.admin import MarkdownxModelAdmin

from pycolos.pycolos.models import Test, Question, Answer, TestSession, UserAnswer

admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(TestSession)
admin.site.register(UserAnswer)


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(MarkdownxModelAdmin):
    inlines = [AnswerInline, ]