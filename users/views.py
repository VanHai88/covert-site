from django.contrib.auth import login
from django.contrib import messages
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from crispy_forms.utils import render_crispy_form
from django.http import JsonResponse

from django.shortcuts import get_object_or_404

from eauth.views import coral_jwt

from .forms import PasswordForm, UserUpdateDetailForm, PasswordChangeForm
from .tokens import account_activation_token
from collections import defaultdict

from attendances.models import Attendance
from courses.models import Course


def signup_complete(request):
    next = request.GET.get('next', '/')

    template = "signup_complete.html"
    template_vars = {'next': next}
    return render(request, template, template_vars)


@login_required
def course_attendance(request):
    user = request.user
    ucountry = user.uprofile.country

    courses = Course.objects.live().filter(countries=ucountry)
    cdict = {obj.id: obj for obj in courses}

    ct_map = defaultdict(dict)
    ctlevels = Course.ctags.through.objects.filter(
        course__in=courses, tag__parent__text='levels')
    ctcerts = Course.ctags.through.objects.filter(
        course__in=courses, tag__parent__text='certs')

    ctcdict = {obj.course_id: obj.tag.text for obj in ctcerts}

    for item in ctlevels:
        ct_map[item.tag.text].setdefault(
            ctcdict.get(item.course_id, 'main'), [])
        ct_map[item.tag.text][ctcdict.get(item.course_id, 'main')].append(
            cdict[item.course_id])

    extras = []

    for obj in Attendance.objects.filter(user=user):
        course = cdict.get(obj.course_id)
        if course:
            cdict[obj.course_id].cdate = obj.date
        else:
            extras.append(obj)

    template = "course_attendance.html"
    template_vars = {'ct_map': ct_map, 'extras': extras}
    return render(request, template, template_vars)


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        data = request.POST
        form = None
        if data.get('user-detail'):
            form = UserUpdateDetailForm(instance=user, data=data)
        elif data.get('password'):
            form = PasswordChangeForm(user, data=data)

        if form.is_valid():
            user = form.save()
            if data.get('password'):
                update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        else:
            form_html = render_crispy_form(form)
            return JsonResponse({
                'success': False,
                'form_html': form_html,
                'errors': form.errors
            })

    update_detail_form = UserUpdateDetailForm(instance=user)
    change_password_form = PasswordChangeForm(user)
    template = "profile.html"
    template_vars = {'updateForm': update_detail_form,
                     'passwordChangeForm': change_password_form}
    return render(request, template, template_vars)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or (not None and not account_activation_token.check_token(user=user, token=token)):
        return render(request, 'account_activation_invalid.html')

    
    user.is_active = True
    user.save()
    coral_jwt(request, user)
    form = None

    
    template = "user_activate.html"
    template_vars = {}
    return render(request, template, template_vars)

