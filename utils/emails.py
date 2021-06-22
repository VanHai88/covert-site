from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_user_mail(subject, user, template, kwargs):
    kwargs['domain'] = 'https://' +  Site.objects.get_current().domain
    from_email, to = settings.DEFAULT_FROM_EMAIL, user.email
    html_content = render_to_string(template, kwargs)
    msg = EmailMultiAlternatives('DPEX Community | ' + subject, '', from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()