from django.db.models import Q

from rest_framework import renderers, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import VideoSerializer

from .models import VideoPage


class VideoViewSet(viewsets.ModelViewSet):
    queryset = VideoPage.objects.all()
    serializer_class = VideoSerializer
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
        cat = self.request.GET.get('cat')

        videos = []
        if search:
            query = Q(title__icontains=search) | Q(description__icontains=search)
            videos = VideoPage.objects.live().filter(query).order_by('?')
        if cat:
            query = Q(ctag=int(cat))
            videos = VideoPage.objects.live().filter(query).order_by('?')
        return videos

    def list(self, request, *args, **kwargs):
        response = super(VideoViewSet, self).list(request, *args, **kwargs)
        if self.request.GET.get('format', 'json') == 'html':
            return Response({'videos': response.data}, template_name='__api_videos.html')
        return response
