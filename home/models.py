import requests

from django.db import models
from django.conf import settings

from collections import defaultdict
from datetime import date, timedelta
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.fields import RichTextField

from collections import defaultdict
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

from advisors.models import AdvisorProfile
from courses.models import Course, CourseSession
from partners.models import Partner
from blog.models import BlogPage, BlogCategory
from events.models import Event
from videos.models import VideoPage
from research.models import ResearchPage
from tools_resources.models import ToolsResources
from updates.models import SiteUpdate

import random

def gen_courses():
    courses = Course.objects.live().filter(promoted=True).order_by('?')
    course_dict = {}

    for obj in courses:
        course_dict[obj.id] = obj 
        obj.bcountry = [str(x).lower() for x in obj.countries if x != 'ON']

    sessions = CourseSession.objects.filter(course_id__in=course_dict.keys()).prefetch_related('session')

    sess_dict = {}
    for item in sorted([x for x in sessions if x.session.dates[0] > (date.today() + timedelta(days=1))], key=lambda x: x.session.dates[0]):
        if not sess_dict.get(item.course_id):
            sess_dict[item.course_id] = item.session.dates

    for k, v in course_dict.items():
        try:
            v.nsess = [sess_dict[k][0].strftime("%e"), sess_dict[k][0].strftime("%b"), sess_dict[k][0].strftime("%Y"), len(sess_dict[k]), sess_dict[k][0]]
        except:
            v.nsess = ['', '', '', '', date.today()]
          
    return sorted(courses[:6], key=lambda x: x.nsess[4])      

def gen_news():
    headers = {'Authorization': settings.BRAIN_KEY, 'Cache-Control': 'no-cache'}
        
    news_dict = {}
    for cty in ['SG', 'PH', 'MY', 'ID', 'TH']:
        payload = {'country':cty}
        req = requests.get("https://brain.genexist.com/apis/news-priv/", headers=headers, params=payload)
        if cty == 'SG':
            news_dict[cty] = req.json()['results'][:3]
        else:
            news_dict[cty] = req.json()['results'][:2]

    return news_dict

class HomePage(Page):

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['partners'] = Partner.objects.exclude(row=0).order_by('row')
        
        context['events'] = Event.objects.live().filter(start__gt=date.today()).order_by('start').distinct()[:3]
        context['videos'] = list(VideoPage.objects.live().order_by('?').distinct())[:5]
        context['research'] = ResearchPage.objects.live().order_by('-first_published_at')[:4]    

        context['courses'] = gen_courses()

        hsdict = defaultdict(list)

        hspec_list = HomeSpecial.objects.all().values_list('blogcat_id', flat=True)
        blog_cats = BlogPage.blog_categories\
                        .through.objects.filter(category_id__in=hspec_list)\
                        .order_by('?')\
                        .prefetch_related('category', 'page')

        for obj in blog_cats:
            hsdict[obj.category.slug].append(obj.page)

        context['quests'] = Question.objects.filter(slug__in=['quest1', 'quest2']).prefetch_related('answers')
        context['special'] = hsdict.get('covid-19', [])[:3]
        context['ind'] = hsdict.get('learning-roadmap', [])[:2]
        context['org'] = hsdict.get('organisations-resources', [])[:2]

        cspecial = context['special'] + context['ind'] + context['org']

        resdict = defaultdict(list)
        resources = ToolsResources.objects.live()
        for item in resources:
            resdict[item.type].append(item)
        
        nresdict = {}
        for k, v in resdict.items():
            random.shuffle(v)
            nresdict[k] = v

        context['resources'] = nresdict

        context['news'] = gen_news()
        context['updates'] = SiteUpdate.objects.all().order_by('-created')[:6]
        context['entries'] = HomePage.objects.child_of(self).live()

        context['articles'] = BlogPage.objects.live().exclude(id__in=[x.id for x in cspecial]).order_by('-date').distinct()[:3]

        return context

@register_snippet
class Question(models.Model):
    text = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, null = True, blank = True,
                on_delete = models.CASCADE, related_name = 'answers')

    answer = models.CharField(max_length=300, null=True)
    url = models.URLField()


class AboutPage(Page):
    pass

    def get_context(self, request):
        context = super(AboutPage, self).get_context(request)
        advisors = AdvisorProfile.objects.all().order_by('order')
        context['advisors'] = advisors
        return context

class StaticPage(Page):
    body = RichTextField(verbose_name='body', blank=True)

    content_panels = [
        FieldPanel('title', classname="full title"),        
        FieldPanel('body', classname="full"),
    ]

class HomeSpecial(models.Model):
    name = models.CharField('Home Special', max_length=50)
    blogcat = models.ForeignKey(BlogCategory, blank=True, null=True, on_delete=models.CASCADE)
    blog = models.ManyToManyField(BlogPage)

