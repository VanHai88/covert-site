from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from wagtail.snippets.models import register_snippet
from taggit.models import Tag

from .abstract import (
    BlogCategoryAbstract,
    BlogCategoryBlogPageAbstract,
    BlogIndexPageAbstract,
    BlogPageAbstract,
    BlogPageTagAbstract
)

class BlogIndexPage(BlogIndexPageAbstract):
    class Meta:
        verbose_name = _('Blog index')

    @property
    def blogs(self):
        # Get list of blog pages that are descendants of this page
        blogs = BlogPage.objects.descendant_of(self).live()
        blogs = blogs.order_by(
            '-date'
        ).select_related('owner').prefetch_related(
            'tagged_items__tag',
            'categories',
            'categories__category',
        )
        return blogs

    def get_context(self, request, tag=None, category=None, author=None, *args,
                    **kwargs):
        context = super(BlogIndexPage, self).get_context(request)
        
        context['cats'] = BlogCategory.objects.all().order_by('order')
        context['catfilter'] = request.GET.get('cat')
        return context

    subpage_types = ['blog.BlogPage']


@register_snippet
class BlogCategory(BlogCategoryAbstract):
    class Meta:
        ordering = ['name']
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")


class BlogCategoryBlogPage(BlogCategoryBlogPageAbstract):
    class Meta:
        pass


class BlogPageTag(BlogPageTagAbstract):
    class Meta:
        pass


@register_snippet
class BlogTag(Tag):
    class Meta:
        proxy = True


def get_blog_context(context):
    """ Get context data useful on all blog related pages """
    context['authors'] = get_user_model().objects.filter(
        owned_pages__live=True,
        owned_pages__content_type__model='blogpage'
    ).annotate(Count('owned_pages')).order_by('-owned_pages__count')
    context['all_categories'] = BlogCategory.objects.all()
    context['root_categories'] = BlogCategory.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        blog_count=Count('blogpage'),
    )
    return context


class BlogPage(BlogPageAbstract):
    class Meta:
        verbose_name = _('Blog page')
        verbose_name_plural = _('Blog pages')

    def get_blog_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blogs'] = self.get_blog_index().blogindexpage.blogs
        context = get_blog_context(context)

        context['cats'] = BlogCategory.objects.all().order_by('order')

        cats = self.categories.values_list('category_id', flat=True)
        related = BlogPage.objects.filter(categories__category_id__in=cats).exclude(id=self.id).distinct()[:3]
        context['related'] = related
        return context

    

    parent_page_types = ['blog.BlogIndexPage']
