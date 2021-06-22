from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django_select2 import forms as s2forms

from .models import Attendance


class UserModelChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.email


class AttendanceUserForm(forms.Form):
    user = UserModelChoice(
        queryset=User.objects.all(),
        label="User",
        to_field_name="username",
        widget=s2forms.Select2Widget
    )


UserAttendaceFormSetBase = modelformset_factory(
    Attendance,
    extra=0,
    fields=('date', 'course')
)


class UserAttendanceFormSet(UserAttendaceFormSetBase):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['date'].widget = forms.DateInput(attrs={
            'class': 'form-control col-6',
            'type': 'date'
        })
        form.fields['course'].widget.attrs['class'] = "form-control col-6"
