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
            container = manager.get(stop)
            container.stop()
            container.remove()
        else:
            image = request.POST.get("IMAGE")
            for plugin in PLUGINS_LIST:
                if plugin.get("image") == image:
                    env = []
                    keys = [environment_variable.get("key") for environment_variable in plugin.get(
                        "configuration").get("environment")]
                    for key, value in request.POST.items():
                        if key in keys:
                            env.append(f"{key}={value}")

                    manager.start(
                        plugin=plugin,
                        env=env
                    )

    started, notstarted = manager.status()

    return render(request, "home/plugins.html", {
        "started": started,
        "notstarted": notstarted
    })
