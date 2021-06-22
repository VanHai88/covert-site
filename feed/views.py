from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.template.context_processors import csrf

from .forms import CreatePostForm
from .models import StreamPost, StreamGroup
from crispy_forms.utils import render_crispy_form
from stream_django.enrich import Enrich
from stream_django.feed_manager import feed_manager

enricher = Enrich()
class main_feed(DetailView):
    model = User
    template_name = 'main_feed.html'
    
    def get_object(self):
        if self.request.user.is_authenticated:
            return self.get_queryset().get(id=self.request.user.id)

    def get_context_data(self, object):
        if not self.object:
            return None
        else:
            user = self.object
            feeds = feed_manager.get_user_feed(user.id)
            try:
                activities = feeds.get()['results']
                activities = enricher.enrich_activities(activities)
            except:
                activities = None
            return {
                'activities': activities,
                'user': user,
                'login_user': self.request.user
            }

@login_required
def ajax_create_post(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        uuid = request.POST.get('uuid')
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(CreatePostForm(), context=ctx)
        
        if not uuid or uuid == "undefined":
            post = None
        else:
            post = StreamPost.objects.get(uuid=uuid)

        if action == 'load':
            form = CreatePostForm(instance=post)
            form_html = render_crispy_form(form, context=ctx)
            return JsonResponse({'success': True, 'form_html': form_html})

        elif action == 'save':
            form = CreatePostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return JsonResponse({'success': True})

            return JsonResponse({'success': False, 'form_html': form_html})
    return JsonResponse({'success': False})

@login_required
def ajax_delete_post(request):
    if request.method == 'POST':
        uuid = request.POST.get('uuid')
        if uuid:
            try:
                post = StreamPost.objects.get(uuid=uuid)
                post.delete()
            except:
                return JsonResponse({'success':False})
            return JsonResponse({'success': True})
        return JsonResponse({'success':False})


class create_stream_post(CreateView):
    # for testing purposes, to be phased out
    # manually create post, which is detected as activity
    template_name = 'activity/create_post.html'
    model = StreamPost
    fields = ['group','title','content']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(StreamPost, self).form_valid(form)

