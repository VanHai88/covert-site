from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject

from .models import SiteData

def current_url(request):
    if settings.DEBUG:
        return {'url': 'http://localhost:8000%s' % request.path }
    else:
        site = SimpleLazyObject(lambda: get_current_site(request))

        return {'current_url': 'https://%s%s' % (site, request.path)}

def site_data(request):
    sdatas = SiteData.objects.all()
    sddict = {obj.key:obj for obj in sdatas}

    return {'sddict':sddict}