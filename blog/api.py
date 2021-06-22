import json

from django.db.models import Q

from collections import defaultdict

from rest_framework import renderers, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .serializers import BlogSerializer

from blog.models import BlogCategoryBlogPage, BlogPage

class BlogViewSet(viewsets.ModelViewSet):
    queryset = BlogPage.objects.all().prefetch_related('author', 'blog_categories')
    serializer_class = BlogSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')

    def get_queryset(self):
        cat_id = self.request.GET.get('cat', '0')
        search = self.request.GET.get('search')

        query = Q()

        if cat_id != '0':
            query &= Q(categories__category=int(cat_id))

        if search:
            query &= (Q(title__icontains=search) | Q(body__icontains=search))

        blogs = BlogPage.objects.live().filter(query).prefetch_related('author')
        blog_dict = {obj.id:obj for obj in blogs}

        cat_dict = defaultdict(list)
        cats = BlogCategoryBlogPage.objects.filter(page__in=blogs).prefetch_related('category')
        
        for cat in cats:
            cat_dict[cat.page_id].append(cat.category.name)

        for k, v in blog_dict.items():
            try:
                v.cat_parsed = cat_dict.get(k)
            except:
                v.cat_parsed = ''

        return blogs.order_by('-date')

    def list(self, request, *args, **kwargs):
        response = super(BlogViewSet, self).list(request, *args, **kwargs)
        
        if self.request.GET.get('format', 'json') == 'html':
            return Response({'blogs': response.data['results'], 'pagination': response.data['pagination']}, template_name='__api_articles.html')
        return response