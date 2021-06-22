import json

from django.db.models import Q

from rest_framework import renderers, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .serializers import TopicSerializer

from machina.apps.forum.models import Forum
from .models import Topic

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().prefetch_related('forum', 'poster', 'first_post')
    serializer_class = TopicSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')

    def get_queryset(self):
        fuuid = self.request.GET.get('forum')
        search = self.request.GET.get('search', '')

        if not fuuid:
            raise APIException('No forum')

        ftags = self.request.GET.get('ftags', '[]')
        tag_list = json.loads(ftags)

        query = Q(forum__uuid=fuuid)

        if tag_list:
            query &= Q(tags__in=tag_list)

        if search:
            query &= (Q(subject__icontains=search) | Q(first_post__content__icontains=search))

        return Topic.objects.filter(query).prefetch_related('tags').order_by('-created')

    def list(self, request, *args, **kwargs):
        response = super(TopicViewSet, self).list(request, *args, **kwargs)
        
        if self.request.GET.get('format', 'json') == 'html':
            return Response({'topics': response.data['results'], 'pagination': response.data['pagination']}, template_name='forum_conversation/topic_list.html')
        return response