import shortuuid

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


def gen_file_name(instance, filename):
    return 'tools-resources/%s.png' % (shortuuid.uuid())


class ToolsResources(Page):
    CHOICES = [
        ('regulators', 'Regulators'),
        ('tools', 'Tools'),
        ('partners', 'Channel Partners'),
        ('learning', 'Accreditation Partners')
    ]
    name = models.CharField(max_length=100)
    url_address = models.URLField()
    description = RichTextField()
    type = models.CharField(choices=CHOICES, default='tools', max_length=100)
    banner = ProcessedImageField(
        upload_to=gen_file_name,
        processors=[ResizeToFill(750, 500)],
        format='PNG',
        options={'quality': 90}, blank=True, null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description', classname="full"),
        FieldPanel('url_address'),
        FieldPanel('type'),
        FieldPanel('banner'),
    ]

    @property
    def get_banner(self):
        if self.banner:
            return self.banner.url
        else:
            return ''


class ToolsResourcesIndex(Page):
    def get_context(self, request):
        context = super().get_context(request)
        page, type = request.GET.get('page'), request.GET.get('type')
        if type:
            items = self.get_children()\
                .live()\
                .filter(toolsresources__type=type)\
                .all()
        else:
            items = self.get_children().live().order_by('toolsresources__type')

        paginator = Paginator(items, 10)

        try:
            items = paginator.get_page(page)
        except PageNotAnInteger:
            items = paginator.get_page(1)
        except EmptyPage:
            items = paginator.get_page(paginator.num_pages)

        context['type'] = request.GET.get('type', '')
        context['items'] = items
        context['choices'] = ToolsResources.CHOICES

        return context
