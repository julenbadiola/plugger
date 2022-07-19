# -*- encoding: utf-8 -*-

from authentication.utils import anonymous_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from authentication.utils import anonymous_required
from .forms import LoginForm
from core.settings import LOGIN_REDIRECT_URL

@anonymous_required
def user_login(request):
    form = LoginForm(request.POST or None)
    msg = None
    status = None
    
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                status = 200
                return redirect(LOGIN_REDIRECT_URL)
            else:
                status = 401
                msg = "Invalid credentials"
        else:
            status = 400
            msg = "Error validating the form"

    return render(request, "login.html", {"form": form, "msg": msg}, status=status)