from django.contrib import admin

# Register your models here.
from markdownx.admin import MarkdownxModelAdmin

from pycolos.pycolos.models import Test, Question, Answer, TestSession, UserAnswer, ForbiddenWord

admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(UserAnswer)


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1


class ForbiddenWordInline(admin.StackedInline):
    model = ForbiddenWord
    extra = 1


@admin.register(Question)
class QuestionAdmin(MarkdownxModelAdmin):
    inlines = [AnswerInline, ForbiddenWordInline]


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'is_finished')

    def is_finished(self, obj):
        return obj.current_index >= len(obj.questions_list.split(','))