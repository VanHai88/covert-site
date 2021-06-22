from django.dispatch import receiver
from utils.emails import send_user_mail
from .tokens import AccountActivationTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from attendances.models import Attendance


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='uprofile')
    company = models.CharField('Company', max_length=300, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    designation = models.CharField(
        "Designation", max_length=200, blank=True, null=True)


def update_user_attendances(user):
    user_attendances = Attendance.objects.filter(email=user.email).all()
    for att in user_attendances:
        att.user = user
        att.email = None
        att.save()


@receiver(post_save, sender=User)
def gen_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()

        template = 'emails/account_activation.html'
        subject = 'Account Activation'
            
        kwargs = {
            'user': instance,
            'uid': urlsafe_base64_encode(force_bytes(instance.id)),
            'token': AccountActivationTokenGenerator().make_token(instance),
        }
        send_user_mail(subject, instance, template, kwargs)
        update_user_attendances(user=instance)
