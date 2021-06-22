import shortuuid
from openpyxl import load_workbook
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet

from courses.models import Course


def gen_file_name(instance, filename):
    return 'courses/%s.png' % (shortuuid.uuid())


class SpecBadge(models.Model):
    badge = ProcessedImageField(
        upload_to=gen_file_name,
        processors=[ResizeToFit(250, 250)],
        format='PNG',
        options={'quality': 90}, blank=True, null=True
    )
    name = models.CharField('Badge Name', max_length=200)


class SpecAssign(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(SpecBadge, on_delete=models.CASCADE)
    date = models.DateField()


class Attendance(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    private = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)


@register_snippet
class AttendanceImport(models.Model):
    file = models.FileField(blank=True, upload_to='temp')

    panels = [
        FieldPanel('file')
    ]

    def _process_attendances(self, attandances):
        for attand in attandances:
            user = User.objects.filter(
                email=attand['email'],
            ).first()
            course = Course.objects.filter(
                id=attand['course_id']
            ).first()
            if course:
                Attendance.objects.create(
                    user=user,
                    course=course,
                    date=attand['date'],
                    private=False,
                    email=attand['email'] if not user else None
                )

    def save(self, *args, **kwargs):
        wb = load_workbook(filename=self.file)
        attendances = []
        for row in wb.active.values:
            try:
                attendance = {
                    'email': row[5],
                    'course_id': row[1],
                    'date': datetime.strptime(
                        '{} {}'.format(row[10], int(row[0])),
                        '%d. %b %Y'
                    )
                }
            except IndexError:
                continue
            attendances.append(attendance)

        self._process_attendances(attendances)
