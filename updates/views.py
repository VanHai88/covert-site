from django.shortcuts import render

from .models import SiteUpdate

# Create your views here.
def all_updates(request):
    updates = SiteUpdate.objects.all().order_by('-created')

    template = "all_updates.html"
    template_vars = {'updates':updates}
    return render(request, template, template_vars)