# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from apps.authentication.token import account_activation_token
from apps.profile.models import Profile
from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                try:
                    user_temp = Profile.objects.get(username=username)
                except ObjectDoesNotExist:
                    user_temp = None

                if user_temp is None:
                    msg = "This account doesn't exist."
                elif not user_temp.is_active:
                    msg = "Inactive account - Please confirm your email or contact support"
                else:
                    msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form_kwargs = {"domain": get_current_site(request).domain}
            form.save(**form_kwargs)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            success = True

            if settings.EMAIL_CONFIRMATION:
                msg = "User created (inactive state). <br />Please confirm your email."
            else:
                msg = 'User created - please <a href="/login">login</a>.'

            # return redirect("/login/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form, "msg": msg, "success": success},
    )


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Profile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        msg = "Your account have been confirmed."
        return render(
            request, "registration/activation.html", {"msg": msg, "success": True}
        )
    else:
        msg = "The confirmation link was invalid, possibly because it has already been used."
        return render(
            request, "registration/activation.html", {"msg": msg, "success": False}
        )
