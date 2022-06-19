# -*- encoding: utf-8 -*-

from core.docker import manager
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from core.utils import anonymous_required
from core.catalogue import PLUGINS_LIST
from django.http import JsonResponse


def status(request):
    started, stopped = manager.status()
    return JsonResponse([plugin.get("info") for plugin in started], safe=False)

@login_required(login_url="/login")
def catalogue_json(request):
    return JsonResponse(PLUGINS_LIST, safe=False)

@login_required(login_url="/login")
def catalogue(request):
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

            manager.start(
                name=name,
                plugin=data,
                request_data=request.POST
            )

    started, notstarted = manager.status()

    return render(request, "catalogue.html", {
        "started": started,
        "notstarted": notstarted
    })
