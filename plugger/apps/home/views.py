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

    containers = manager.list()
    for plugin in PLUGINS_LIST:
        found = False
        for container in containers:
            container: Container
            if plugin.get("image") in container.image.attrs.get("RepoTags"):
                plugin["containerId"] = container.id
                started.append({**plugin, **container.__dict__})
                found = True
        if not found:
            notstarted.append(plugin)

    context = {
        "segment": "plugins",
        "started": started,
        "notstarted": notstarted
    }
    html_template = loader.get_template("home/plugins.html")
    return HttpResponse(html_template.render(context, request))
