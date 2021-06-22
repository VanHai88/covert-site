import shortuuid

from django.db import models

from wagtail.snippets.models import register_snippet

@register_snippet
class SiteUpdate(models.Model):
    url = models.URLField()
    name = models.CharField('Name', max_length=300)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name