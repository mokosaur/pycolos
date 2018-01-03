from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from markdownx.models import MarkdownxField

from pycolos.pycolos.helpers import markdown_to_html
from pycolos.pycolos.receivers import *


class Test(models.Model):
    """Test containing questions defined to be solved by students."""
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available_from = models.DateTimeField(null=True)
    available_for_x_minutes = models.IntegerField(null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Test: " + self.name


class Question(models.Model):
    """Question which belongs to a test."""
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    DIFFICULTY_LEVELS = (
        ('VE', 'Very Easy'),
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
        ('VH', 'Very Hard'),
    )
    QUESTION_TYPES = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    difficulty = models.CharField(max_length=100, choices=DIFFICULTY_LEVELS)
    type = models.CharField(max_length=100, choices=QUESTION_TYPES)
    question_text = MarkdownxField()
    tests = models.TextField(blank=True)

    def __str__(self):
        return self.question_text

    @property
    @mark_safe
    def formatted_markdown(self):
        return markdown_to_html(self.question_text)


class Answer(models.Model):
    """Possible answer that can be defined below a closed test question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)

    def __str__(self):
        return self.answer_text


class TestSessionManager(models.Manager):
    def create_session(self, user, test, order):
        very_easy = Question.objects.filter(test=test, difficulty='VE').order_by('?')
        easy = Question.objects.filter(test=test, difficulty='E').order_by('?')
        medium = Question.objects.filter(test=test, difficulty='M').order_by('?')
        hard = Question.objects.filter(test=test, difficulty='H').order_by('?')
        very_hard = Question.objects.filter(test=test, difficulty='VH').order_by('?')
        levels = [very_easy, easy, medium, hard, very_hard]
        if order == "easy":
            questions_list = ",".join(",".join(str(q.id) for q in l) for l in levels if l)
        else:
            questions_list = ",".join(",".join(str(q.id) for q in l) for l in reversed(levels) if l)
        test_session = self.create(user=user, test=test, questions_list=questions_list)
        return test_session


class TestSession(models.Model):
    """Session of the examination. Every time any user starts an examination, the test session is created for him"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    questions_list = models.CharField(validators=[validate_comma_separated_integer_list], max_length=1000, default="")
    current_index = models.IntegerField(default=0)
    objects = TestSessionManager()

    def __str__(self):
        return self.user.username + " " + self.test.name


class UserAnswer(models.Model):
    """Answer that was given by a student during his examination."""
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
