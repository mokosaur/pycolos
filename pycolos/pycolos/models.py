from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField

from pycolos.pycolos.receivers import *


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available_from = models.DateTimeField(null=True)
    available_for_x_minutes = models.IntegerField(null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Test: " + self.name


class Question(models.Model):
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


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)

    def __str__(self):
        return self.answer_text


class TestSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)


class UserAnswer(models.Model):
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
