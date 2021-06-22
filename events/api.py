import json

from django.db.models import Q

from collections import defaultdict
from datetime import date

from rest_framework import renderers, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .serializers import EventSerializer

from .models import Event

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    pagination_class = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='event_detail.html')

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        year = self.request.GET.get('year', '')
        month = self.request.GET.get('month', '')

        query = Q()
        
        if year:
            query &= Q(start__year=int(year))

        if month:
            query &= Q(start__month=int(month))

        if search:
            query &= Q(title__icontains=search)

        if not year and not month and not search:
            query &= Q(start__gte=date.today())

        return Event.objects.live().filter(query).order_by('start')

    def list(self, request, *args, **kwargs):
        response = super(EventViewSet, self).list(request, *args, **kwargs)
        
        if self.request.GET.get('format', 'json') == 'html':
            return Response({'events': response.data}, template_name='__api_events.html')
        return response