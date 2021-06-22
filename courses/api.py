import json

from django.db.models import Q

from collections import defaultdict
from datetime import date, timedelta

from rest_framework import renderers, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .serializers import CourseSerializer

from .models import Course, CourseSession
from utils.models import Tag

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)
    pagination_class = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='course_detail.html')

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        cert = self.request.GET.get('cert', '')
        location = self.request.GET.get('location', '')
        
        query = Q()

        if cert:
            query &= Q(ctags__in=[int(cert)])

        if location:
            query &= Q(countries__contains=location)

        if search:
            query &= (Q(title__icontains=search) | Q(description__icontains=search))
        
        courses = Course.objects.filter(query)
        
        course_dict = {obj.id:obj for obj in courses}

        sess_dict = {}
    
        sessions = CourseSession.objects.filter(course__in=courses).prefetch_related('session')
        for item in sorted([x for x in sessions if x.session.dates[0] > (date.today() + timedelta(days=1))], key=lambda x: x.session.dates[0]):
            if not sess_dict.get(item.course_id):
                sess_dict[item.course_id] = item.session.dates
            
        for k, v in course_dict.items():
            if sess_dict.get(k):
                v.next_session = [sess_dict[k][0].strftime("%e"), sess_dict[k][0].strftime("%b"), sess_dict[k][0].strftime("%Y"), len(sess_dict[k]), sess_dict[k][0]]
            else:
                v.next_session = ['','','','', date.today() + timedelta(days=365)]

        return courses

    def list(self, request, *args, **kwargs):
        response = super(CourseViewSet, self).list(request, *args, **kwargs)

        if self.request.GET.get('format', 'json') == 'html':

            return Response({'courses': response.data}, template_name='__api_courses.html')
        return response