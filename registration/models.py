from django.contrib.auth.models import User
from django.db import models

from events.models import Event
from courses.models import Course


SCHOICES = (
        ('confirmed', 'Confirmed'),
        ('attended', 'Attended')
    )
# Create your tests here.
class Registration(models.Model):
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField('Status', choices=SCHOICES, max_length=50)