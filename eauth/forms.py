import shortuuid

from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _


from crispy_forms.bootstrap import StrictButton, FieldWithButtons, InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, HTML, Layout, Submit
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from intl_tel_input.widgets import IntlTelInputWidget

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email_auth = forms.EmailField()
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 vcenter'
        self.helper.field_class = 'col-8'
        self.helper.form_id = 'loginForm'
        self.helper.form_method = 'post'
        self.fields['email_auth'].label = "Email"
        self.helper.layout = Layout(            
            'email_auth',
            'password',
            Div(
                Div(StrictButton('Login', css_class='btn btn-long btn-primary'), css_class='col-6'),
                HTML('<div class="col-6 text-right"><a class="otext" href="/accounts/password/reset/">Forgot Password?</a></div>'),
            css_class='row vcenter'),
        )

    def clean(self):
        email = self.cleaned_data.get('email_auth')

        error = False
        if email:
            user = User.objects.filter(email=email.lower())
            if not user:
                error = True
        else:
            error = True        

        if error:
            raise forms.ValidationError('Please enter a valid email and password!')

        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=user[0].username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Please enter a valid email and password!')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        pass
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        '''
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',

            )
        '''

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):

        return self.user_cache

class UserCreationForm(forms.ModelForm):
    terms = forms.BooleanField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        validators=[validate_password,]
    )
    country = CountryField().formfield()
    company = forms.CharField()


    
    class Meta:
        model = User
        fields = ("first_name", "email", 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-4 vcenter'
        self.helper.field_class = 'col-8'
        self.helper.form_id = 'signupForm'
        self.helper.form_method = 'post'
        self.helper.include_media = False

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['terms'].required = True
        self.fields['email'].label = 'Email'
        self.fields['company'].required = False

        self.fields['terms'].label = 'I have read the <a class="otext" href="/terms-and-conditions/" target="_blank">terms and conditions</a> and <a class="otext" href="/privacy-policy/" target="_blank">privacy policy</a>.'

        self.fields['password'].help_text='Password should have a minimum length of 8'
        self.helper.layout = Layout(
            'email',
            'first_name',
            'last_name',
            'company',
            'country',
            FieldWithButtons('password', StrictButton('<i class="fa fa-eye"></i>', css_class="btn-primary passToggle")),
            Div(
                Div(InlineField('terms'), css_class="col-md-12"),
                css_class='row mb-4'
            ),
            StrictButton('Signup', css_class='btn btn-long btn-primary usignup'),
                
            HTML('<div class="row mt-4"><div class="col-md-12 text-center"><p><small>By signing up, I consent to my personal information being used for the purpose of \
                  providing membership services offered in the DPEX network portal. This includes being able to access courses, videos, discussion \
                  forums, and training records from an affiliated university as well as receiving email updates to complement my learning journey.</small></p></div></div>'),
        )

    def clean(self):
        email = self.cleaned_data.get('email').lower()
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError('Please enter a valid email!')

    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.username = shortuuid.uuid()

        user.email = self.cleaned_data["email"].lower()
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password"])
        user.save()
        
        user.uprofile.country = self.cleaned_data["country"]
        user.uprofile.company = self.cleaned_data["company"]
        user.uprofile.save()

        return user