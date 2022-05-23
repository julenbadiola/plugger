# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.authentication.token import account_activation_token
from apps.profile.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )

    class Meta:
        model = Profile
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True, *args, **kwargs):
        domain = kwargs.get("domain")
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if not settings.EMAIL_CONFIRMATION:
            if commit:
                user.save()
            return user

        user.is_active = False

        if commit:
            user.save()

        # Sending email
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        subject = "Activate your account"
        message = (
            f"This is your activation link. http://{domain}/activate/{uid}/{token}/"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        return user


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            Profile.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError("No user exists with this email")

        return email
