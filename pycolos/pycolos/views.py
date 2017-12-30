from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import UserForm


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


def logout_view(request):
    logout(request)
    return redirect('index')
