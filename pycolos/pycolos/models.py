from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


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
    question = models.TextField()
    tests = models.TextField(blank=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)


class TestSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)


class UserAnswer(models.Model):
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
