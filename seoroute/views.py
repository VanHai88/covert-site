from django.shortcuts import get_object_or_404, render, redirect

from .models import Route

# Create your views here.
def seo_redirect(request, resource=None):
    host = request.META['HTTP_HOST']

    if not resource:
        return redirect('https://www.dpexnetwork.org/', permanent=True)
    else:
        route = get_object_or_404(Route, old=resource)
        return redirect('https://www.dpexnetwork.org/' + route.new, permanent=True)

