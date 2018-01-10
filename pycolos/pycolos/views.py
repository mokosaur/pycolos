import datetime
import re

from django.http import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse

from pycolos.pycolos.helpers import ProgressBar
from .forms import UserForm
from .models import Test, TestSession, Question, Answer, UserAnswer, messages
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
import string
import random
from django.utils import timezone
from django.core import serializers


def index(request):
    """The index page which displays all available tests for a logged-in user"""
    tests = Test.objects.all()
    return render(request, "index.html", {"tests": tests})


def show_test(request, test_id):
    """Test view which serves the current question in a test session"""
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return Http404("Test o numerze " + test_id + " nie istnieje")
    try:
        test_session = TestSession.objects.get(test=test, user=request.user)
    except TestSession.DoesNotExist:
        if test.available_from > timezone.now():
            messages.add_message(request, messages.WARNING, 'Ten test nie jest jeszcze dostępny')
            return redirect('index')
        test_session = TestSession.objects.create_session(request.user, test, request.GET.get("order"))
    question_index = test_session.current_index
    question_count = test_session.test.question_set.count()
    test_end = test.available_from + datetime.timedelta(minutes=test.available_for_x_minutes)
    if question_index >= question_count or timezone.now() > test_end:
        test_session.current_index = question_count
        test_session.save()
        return render(request, "finish.html")
    question_id = int(test_session.questions_list.split(",")[question_index])
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        if question.type == 'O':
            answer = request.POST.get('answer')
        else:
            answer = request.POST.getlist('answer')
        UserAnswer.objects.create(session=test_session, question=question, answer_text=answer)
        if question.forbiddenword_set.count() > 0:
            for word in question.forbiddenword_set.all():
                r_string = r"\b" + word.word + r"\b"
                if re.search(r_string, answer):
                    messages.add_message(request, messages.ERROR, 'Użyłeś niedozwolonego słowa')
                    return redirect('/show_test/%s/' % test_id)
        test_session.current_index += 1
        test_session.save()
        return redirect('/show_test/%s/' % test_id)
    progress = ProgressBar(question_index, question_count)
    return render(request, 'test.html', {'question': question, 'test_id': test_id, 'progress': progress,
                                         'test_end': test_end})


@staff_member_required
def newuser(request):
    """View that allows a superuser to create student accounts"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            groups = form.cleaned_data.get('group')
            for g in groups:
                g.user_set.add(user)
            messages.add_message(request, messages.SUCCESS, 'Użytkownik został stworzony.')
            return redirect('create_user')
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})


@staff_member_required
def import_export(request):
    """View that allows a superuser to import and export tests"""
    if request.method == 'POST':
        pass
    tests = Test.objects.all()
    return render(request, 'test_export.html', {'tests': tests})


@staff_member_required
def export_test(request):
    """Endpoint that serves a JSON file with a serialized test model"""
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        if test_id != '-':
            test = Test.objects.get(id=int(test_id))
            all_objects = [test] + list(Question.objects.filter(test=test)) + \
                          list(Answer.objects.filter(question__test=test))
            models = serializers.serialize('json', all_objects)
            response = HttpResponse(models, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="test.json"'
            return response
        else:
            pass
    return redirect('import_export')


@staff_member_required
def import_test(request):
    """Endpoint that allows to import a serialized test"""
    if request.method == 'POST':
        pass  # to be done


@staff_member_required
def download_answers(request, test_id):
    """Endpoint that allows a superuser to download all collected answers for a given test"""
    questions = Question.objects.filter(test_id=test_id).order_by('id')
    question_ids = [q.id for q in questions]
    df = pd.DataFrame(columns=['user'] + question_ids)
    users = User.objects.all()
    for u in users:
        answers = {'user': u.username}
        for i in question_ids:
            user_answer = UserAnswer.objects.filter(session__user_id=u.id, question_id=i).last()
            answers[i] = user_answer.answer_text if user_answer else ''
        df = df.append(answers, ignore_index=True)
    response = HttpResponse(df, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="answers.csv"'
    df.to_csv(response, index=False, sep=';')
    return response


@staff_member_required
def download_questions(request, test_id):
    """Endpoint that allows a superuser to download all collected answers for a given test"""
    questions = Question.objects.filter(test_id=test_id).order_by('id')
    df = pd.DataFrame(columns=['question id', 'question', 'tests', 'additional tests'])
    for q in questions:
        df = df.append({
            'question id': q.id,
            'question': q.question_text,
            'tests': q.tests,
            'additional tests': q.additional_tests
        }, ignore_index=True)
    response = HttpResponse(df, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="questions.csv"'
    df.to_csv(response, index=False, sep=';')
    return response


@staff_member_required
def create_users_with_csv(request):
    """Endpoint that creates student accounts given USOS CSV file, and generates a CSV file with user passwords"""
    if request.method == 'POST':
        f = request.FILES['file']
        with open('users.csv', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        df = pd.read_csv('users.csv', sep=';')
        alphabet = string.ascii_letters + string.digits
        res = df[["indeks", "imie", "nazwisko"]]
        res['login'] = res.apply(lambda x: "z" + str(int(x.indeks)), axis=1)
        res['password'] = res.apply(lambda _: ''.join(random.choice(alphabet) for _ in range(8)), axis=1)
        print(res.head())

        for index, row in res.iterrows():
            User.objects.create_user(row.login, password=row.password)

        response = HttpResponse(res, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="generated.csv"'
        res.to_csv(response, index=False)
        return response
