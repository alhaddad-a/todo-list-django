from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import Register

def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = Register()
    return render(request, "register.html", {"form": form})