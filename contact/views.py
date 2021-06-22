import requests

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

def contact_us(request):
    if request.method == 'POST' and not request.POST.get('honeypot', ''):
        message = ''

        ckey = settings.CAPTCHA_KEY
        vurl = "https://hcaptcha.com/siteverify"
        token = request.POST.get('h-captcha-response', '')

        req = requests.post(vurl, data={'secret':ckey, 'response':token})

        if req.json()['success']:
            for k, v in request.POST.items():
                if k not in ['csrfmiddlewaretoken', 'g-recaptcha-response', 'h-captcha-response', 'honeypot']:
                    if k == 'enquiry':
                        message += '%s -- %s\n\n' % (k, '; '.join(request.POST.getlist('enquiry')))
                    else:
                        message += '%s -- %s\n\n' % (k, v)

            send_mail(
                'DPEX Network Request',
                message,
                'mail@support.dpexnetwork.org',
                ['support@dpexnetwork.org'],
                fail_silently=False,
            )

            messages.success(request, 'Your enquiry has been received!')

        return redirect('contact-us')


    template = "contact_us.html"
    template_vars = {}
    return render(request, template, template_vars)