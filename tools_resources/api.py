from django.db.models import Q

from rest_framework import renderers, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import ToolsResourcesSerializer

from .models import ToolsResources


class ToolsResourceViewSet(viewsets.ModelViewSet):
    queryset = ToolsResources.objects.all()
    serializer_class = ToolsResourcesSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    pagination_class = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response(
            {'user': self.object},
            template_name='user_detail.html'
        )

    def get_queryset(self):
        search = self.request.GET.get('search')
        type = self.request.GET.get('type')

        query = Q()

        if type != '':
            query &= Q(type=type)

        if search:
            query &= (
                Q(title__icontains=search) | Q(
                    description__icontains=search)
            )
        items = ToolsResources.objects.live().filter(query).order_by('title')

        return items

    def list(self, request, *args, **kwargs):
        response = super(ToolsResourceViewSet, self).list(request, *args, **kwargs)

        if self.request.GET.get('format', 'json') == 'html':
            return Response({'items': response.data,},
                template_name='__api_resources.html')

        return response
