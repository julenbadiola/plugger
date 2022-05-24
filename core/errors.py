from django.http import HttpResponse
from django.template import loader


def error_404(request, exception):
    context = {}
    html_template = loader.get_template("home/page-404.html")
    return HttpResponse(html_template.render(context, request))


def error_500(request):
    context = {}
    html_template = loader.get_template("home/page-500.html")
    return HttpResponse(html_template.render(context, request))
