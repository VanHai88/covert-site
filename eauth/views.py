import jwt
import requests

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse, resolve

from crispy_forms.utils import render_crispy_form
from datetime import datetime

from .forms import AuthenticationForm, UserCreationForm

def coral_jwt(request, user):
    payload = {
        "user": {
            "id": user.username,
            "email": user.email,
            "username": user.get_full_name()
        }
    }

    request.session['coral_token'] = jwt.encode(payload, settings.CORAL_KEY , algorithm='HS256').decode("utf-8") 


def elogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(None, request.POST or None)

        if form.is_valid():
            user = User.objects.get(email=form.data.get('email_auth').lower())
            auser = authenticate(username=user.username, password=form.data.get('password'))

            if user.is_active:
                coral_jwt(request, auser)


            login(request, auser, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')

            return JsonResponse({'success': True, 'user': auser.get_full_name()})
        # RequestContext ensures CSRF token is placed in newly rendered form_html
        form_html = render_crispy_form(form)
        return JsonResponse({'success': False, 'form_html': form_html, 'errors': form.errors})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()

            payload = {'Name': user.get_full_name(), 
                       'Email': user.email,
                       'HasExternalDoubleOptIn': True,
                       'CustomFields' : [
                            'Country=%s' % str(user.uprofile.country) ,
                            'Company=%s' % user.uprofile.company,
                            'First Name=%s' % user.first_name,
                            "Last Name=%s" % user.last_name,
                        ]
                    }

            url = 'https://api.moosend.com/v3/subscribers/5e53f2a2-d610-4663-bcbf-28c69a8a8f7b/subscribe.json?apikey=%s' % settings.MOO_API
            r = requests.post(url, json=payload)

            auser = authenticate(username=user.username, password=form.data.get('password'))
            login(request, auser, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')

            return JsonResponse({'success': True, 'user':auser.get_full_name()})

        form_html = render_crispy_form(form)
        return JsonResponse({'success': False, 'form_html': form_html, 'errors': form.errors}) 