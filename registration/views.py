import requests

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from .models import Registration
from events.models import Event, BM_SETTINGS
from courses.models import Course

# Create your views here.
@login_required
def submit_reg(request, etype, pid):
    if etype not in ['event', 'course']:
        raise Http404

    event = None
    course = None

    user = request.user
    if etype == 'event':
        event = get_object_or_404(Event, id=pid)
        reg, created = Registration.objects.get_or_create(event=event, user=user, status='confirmed')
        
        if created and event.etype == 'webinar':
            headers = {'API-KEY': BM_SETTINGS['key']}
            payload = {"id": event.bm_id, "email": user.email, 
                       "first_name": user.first_name,
                       "last_name": user.last_name}
            r = requests.put(BM_SETTINGS['url'] + 'conferences/register', headers=headers, data=payload)

        return redirect('complete-reg', etype, pid)
    else:
        course = get_object_or_404(Course, id=pid)
        Registration.objects.create(course=course, user=user, status='confirmed')

    

@login_required
def complete_reg(request, etype, pid):

    if etype not in ['event', 'course']:
        raise Http404

    item = None
    
    if etype == 'event':
        event = get_object_or_404(Event, id=pid)
        item = event
    else:
        course = get_object_or_404(Course, id=pid)
        item = course

    template = "complete_reg.html"
    template_vars = {'item':item}
    return render(request, template, template_vars)
