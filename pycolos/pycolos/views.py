from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
import string
import random


def index(request):
    return render(request, "index.html")


@staff_member_required
def newuser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            return redirect('create_user')
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})


@staff_member_required
def create_users_with_csv(request):
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
