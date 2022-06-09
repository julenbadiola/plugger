# -*- encoding: utf-8 -*-

from apps.docker import Container, manager
from apps.utils import anonymous_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from apps.utils import anonymous_required
from apps.catalogue import PLUGINS_LIST
from .forms import LoginForm
from django.http import JsonResponse


def status(request):
    started, stopped = manager.status()
    return JsonResponse([plugin.get("info") for plugin in started], safe=False)

@login_required(login_url="/")
def list(request):
    return JsonResponse(PLUGINS_LIST, safe=False)


@anonymous_required
def home(request):
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
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "home/login.html", {"form": form, "msg": msg})


@login_required(login_url="/")
def plugins(request):
    started = []
    notstarted = []
    if request.method == 'POST':
        stop = request.POST.get("stop")
        if stop:
            manager.remove(stop)
        else:
            name = request.POST.get("name")
            data = PLUGINS_LIST[name]
            if not data.get("show", True):
                raise Exception("eo")
            
            env = [i["key"] + "=" + i["value"] for i in data.get("configuration", {}).get("system", [])]
            conf_vars = [cv["key"] for cv in data.get("configuration", {}).get("editable", [])]
            [env.append(f"{key}={value}") for key, value in request.POST.items() if key in conf_vars]
            manager.start(
                name=name,
                plugin=data,
                env=env
            )

    started, notstarted = manager.status()

    return render(request, "home/plugins.html", {
        "started": started,
        "notstarted": notstarted
    })
