from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Course

@login_required
def users_list(request):
    users = User.objects.all()

    template = "courses/users_list.html"
    template_vars = {'users': users}
    return render(request, template, template_vars)


@login_required
def all_courses(request):
    courses = Course.objects.all().order_by('id')

    template = "courses/courses_list.html"
    template_vars = {'courses': courses}
    return render(request, template, template_vars)
