# -*- encoding: utf-8 -*-

from core import docker
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from docker.models.containers import Container


# @login_required(login_url="/login/")
def index(request):
    context = {"segment": "index"}
    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))

def plugins(request):
    started = []
    notstarted = []
    if request.method == 'POST':
        stop = request.POST.get("stop")
        if stop:
            container = docker.get(stop)
            container.stop()
            container.remove()
        else:
            image = request.POST.get("IMAGE")    
            for plugin in docker.plugins_list:
                if plugin.get("image") == image:
                    env = []
                    keys = [environment_variable.get("key") for environment_variable in plugin.get("configuration").get("environment")]
                    for key, value in request.POST.items():
                        if key in keys:
                            env.append(f"{key}={value}")

                    docker.create(
                        image=image, 
                        plugin=plugin,
                        env=env
                    )

    containers = docker.list()
    for plugin in docker.plugins_list:
        found = False
        for container in containers:
            container : Container
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


def dashboard(request):
    started = []
    notstarted = []

    context = {
        "segment": "dashboard", 
        "started": started,
        "notstarted": notstarted
    }
    html_template = loader.get_template("home/dashboard.html")
    return HttpResponse(html_template.render(context, request))
