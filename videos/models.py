import shortuuid

from django.db import models

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from utils.models import Tag

def gen_file_name(instance, filename):
    return 'videos/%s.png' % (shortuuid.uuid())


class ModelFieldPanel(FieldPanel):
    def on_form_bound(self):
        self.form.fields['ctag'].queryset = Tag.objects.filter(parent__text='videos')
        super().on_form_bound()


class VideoPage(Page):
    name = models.CharField(max_length=100)
    url_address = models.URLField()
    view_count = models.PositiveIntegerField(default=0)
    description = RichTextField()
    banner = ProcessedImageField(
        upload_to=gen_file_name,
        processors=[ResizeToFill(750, 500)],
        format='JPEG',
        options={'quality': 80}, blank=True, null=True
    )   

    banner_thumb = ImageSpecField(source='banner',
                                      processors=[ResizeToFill(300, 197)],
                                      format='JPEG',
                                      options={'quality': 65})

    
    ctag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description', classname="full"),
        FieldPanel('url_address'),
        FieldPanel('banner'),
        ModelFieldPanel('ctag'),
    ]

    uuid = models.CharField('UUID', max_length=50, default='')
    

    def save(self, *args, **kwargs):
        if not self.id:
            self.uuid = shortuuid.uuid()

        return super().save(*args, **kwargs)


    @property
    def get_banner(self):
        if self.banner:
            return self.banner.url
        else:
            return ''

    @property
    def get_banner_thumb(self):
        if self.banner:
            return self.banner_thumb.url
        else:
            return ''

    def serve(self, request):
        if request.method == 'GET':
            self.view_count += 1
            self.save()

        return super().serve(request)


    def get_context(self, request):
        context = super().get_context(request)
        context['videos'] = VideoPage.objects.filter(ctag=self.ctag_id).exclude(id=self.id).distinct().order_by('?')[:4]
        return context



class VideoPageIndex(Page):
    subpage_types = ['videos.VideoPage']


    def get_context(self, request):
        context = super().get_context(request)
        tags = Tag.objects.filter(parent__text='videos').prefetch_related('parent').order_by('text')
        context['tags'] = tags
        context['videos'] = VideoPage.objects.live().order_by('?')[:3]
        
        return context
