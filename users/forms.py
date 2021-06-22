from django import forms
from django_countries.fields import CountryField
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, HTML, Layout, Submit


class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput,
        strip=False,
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput,
        strip=False,
    )

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('user')
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = False

        self.fields['password'].widget.attrs['placeholder'] = _('Password')
        self.fields['password2'].widget.attrs['placeholder'] = _(
            'Confirm Password')

        for k, v in self.fields.items():
            if k == 'country':
                iclass = 'uk-select'
            else:
                iclass = 'uk-input'

            self.fields[k].label = ''
            self.fields[k].widget.attrs['required'] = True
            self.fields[k].widget.attrs['class'] = iclass

        self.helper.layout = Layout(
            Div(HTML('<input type="hidden" name="vfc9KYAA9" >')),
            Div(HTML('<input type="hidden" name="user" value="%s" >' % uid)),
            Div('password', css_class='uk-margin'),
            Div('password2', css_class='uk-margin'),
            ButtonHolder(
                Submit('submit', _('Save'),
                       css_class='btn-long uk-button uk-button-primary')
            )
        )

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                user = User.objects.get(id=int(self.data['user']))
                password_validation.validate_password(password, user)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self):
        user = User.objects.get(id=int(self.data['user']))
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        user.save()

        return user


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-8'
        self.helper.form_id = 'securitySettingForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2',
            Div(HTML('<input type="hidden" name="password" value="true">')),
            StrictButton(
                'Update', css_class='btn btn-long btn-primary', type='submit'),
        )


class UserUpdateDetailForm(forms.ModelForm):
    country = CountryField().formfield()
    company = forms.CharField()

    class Meta:
        model = User
        fields = ("first_name", "email", 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 vcenter'
        self.helper.field_class = 'col-8'
        self.helper.form_id = 'updateDetail'
        self.helper.form_method = 'post'

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['company'].required = False
        self.fields['country'].initial = kwargs['instance'].uprofile.country

        self.helper.layout = Layout(
            Field('email', readonly=True),
            'first_name',
            'last_name',
            Field('company', required=False, value=kwargs['instance'].uprofile.company),
            'country',
            Div(HTML('<input type="hidden" name="user-detail" value="true">')),
            StrictButton(
                'Update', css_class='btn btn-long btn-primary update-detail'),
        )

    def clean_email(self):
        return self.instance.email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()

        user.uprofile.country = self.cleaned_data["country"]
        user.uprofile.company = self.cleaned_data["company"]
        user.uprofile.save()

        return user
