import requests

from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from datetime import date, timedelta


# Create your views here.

def all_news(request):
    drange = '%s - %s' % (str(date.today() - timedelta(days=30)), str(date.today()))
    country = request.GET.get('country', '')

    template = "all_news.html"
    template_vars = {'drange':drange, 'country':country}
    return render(request, template, template_vars)


def view_news(request, uuid):
    headers = {'Authorization': settings.BRAIN_KEY, 'Cache-Control': 'no-cache'}
    req = requests.get("https://brain.genexist.com/apis/news-priv/%s" % uuid, headers=headers)

    

    if req.status_code == 200:
        news = req.json()
    else:
        raise Http404


    template = "view_news.html"
    template_vars = {'news':news}
    return render(request, template, template_vars)