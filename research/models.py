import shortuuid

from django.db import models
from django.http import JsonResponse

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


def gen_file_name(instance, filename):
    return 'research/{0}_{1}'.format(shortuuid.uuid(), filename)


def gen_banner_name(instance, filename):
    return 'research/%s.png' % (shortuuid.uuid())


class ResearchPage(Page):
    name = models.CharField(max_length=100)
    description = RichTextField()
    view_count = models.PositiveIntegerField(default=0)
    pdf = models.FileField(upload_to=gen_file_name, blank=False)
    banner = ProcessedImageField(
        upload_to=gen_banner_name,
        processors=[ResizeToFill(750, 500)],
        format='PNG',
        options={'quality': 90},
        blank=True,
        null=True
    )

    uuid = models.CharField('UUID', max_length=50, default='')

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description', classname="full"),
        FieldPanel('banner'),
        FieldPanel('pdf'),
    ]

    @property
    def get_banner(self):
        if self.banner:
            return self.banner.url
        else:
            return ''

    def serve(self, request):
        if request.method == 'GET':
            self.view_count += 1
            self.save()
        return super().serve(request)

    def save(self, *args, **kwargs):
        if not self.id:
            self.uuid = shortuuid.uuid()

        super(ResearchPage, self).save(*args, **kwargs)


class ResearchPageIndex(Page):
    subpage_types = ['research.ResearchPage']

    def get_context(self, request):
        context = super().get_context(request)
        items = self.get_children().live().order_by('first_published_at')
        context['items'] = items
        return context
