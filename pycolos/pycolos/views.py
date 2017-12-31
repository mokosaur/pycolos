from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import UserForm
import pandas as pd
import string
import random


def index(request):
    return render(request, "index.html")


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


def create_users_with_csv(request):
    if request.method == 'POST':
        f = request.FILES['file']
        with open('users.csv', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        df = pd.read_csv('users.csv', sep=';')
        alphabet = string.ascii_letters + string.digits

        for row in df.iterrows():
            print(row.indeks, row.imie, row.nazwisko)
            password = ''.join(random.choice(alphabet) for i in range(8))
            pd.DataFrame(data={'indeks': row.indeks,
                               'imie': row.imie,
                               'nazwisko': row.nazwisko,
                               'login': row.indeks,
                               'haslo': password})
        return redirect('create_user')
