# -*- encoding: utf-8 -*-

from apps.docker import Container, manager
from apps.utils import anonymous_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from apps.utils import anonymous_required
from core.catalogue import PLUGINS_LIST
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
            manager.remove(container=stop)
        else:
            name = request.POST.get("name")
            data = PLUGINS_LIST[name]
            if not data.get("show", True):
                raise Exception("eo")
            
            # Get environment variables of the plugin
            env_list = data.get("configuration", {}).get("environment", [])
            
            # Create a env list for all the environment variables
            env = []
            for environment_variable in env_list:
                key = environment_variable["key"]
                value = ""

                # first check if in POST data if the variable is editable
                if environment_variable.get("editable", False):
                    if form_value := request.POST.get(key, None):
                        value = form_value
                        
                # If not value, get the value by default
                if not value:
                    value = environment_variable.get("value", None)
                
                # If there is no value yet and the variable is not optional, raise Exception
                if not value and not environment_variable.get("optional", False):
                    raise Exception(f"Value for {key} not present")

                env.append(key + "=" + value)

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
