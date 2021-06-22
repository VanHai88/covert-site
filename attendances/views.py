from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Attendance
from .forms import UserAttendanceFormSet, AttendanceUserForm


@login_required
def att_list(request):
    if request.method == 'POST':
        data = request.POST
        user_form = AttendanceUserForm(data)
        if user_form.is_valid():
            atts_list = Attendance.objects.in_bulk(data.get('att'))
            for (key, att) in atts_list.items():
                att.user = user_form.cleaned_data['user']
                att.save()
    else:
        user_form = AttendanceUserForm()
    atts = Attendance.objects.filter(user=None, email__isnull=False).all()
    template = "attendances/att_list.html"
    template_vars = {'atts': atts, 'user_form': user_form}
    return render(request, template, template_vars)


@login_required
def user_att_detail(request, username):
    atts = Attendance.objects.filter(user__username=username).all()
    if request.method == 'POST':
        formset = UserAttendanceFormSet(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = UserAttendanceFormSet(queryset=atts)
    template = "attendances/user_atts_list.html"
    template_vars = {'formset': formset, 'username': username}
    return render(request, template, template_vars)
