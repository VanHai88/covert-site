from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin

from machina import urls as machina_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

if settings.SITE_ID == 1:
    ##OLD ROUTES
    urlpatterns = [
        path('', include('seoroute.urls')),
    ]
else:
    urlpatterns = [
        path('dadmin/', admin.site.urls),
        path('admin/', include(wagtailadmin_urls)),
        path('auth/', include('eauth.urls')),
        path('accounts/', include('allauth.urls')),
        path('api/', include('apis.urls')),
        path('articles/', include('blog.urls')),
        path('attendances/', include('attendances.urls')),
        path('contact-us/', include('contact.urls')),
        path('documents/', include(wagtaildocs_urls)),
        path('discussions/', include(machina_urls)),
        path('froala_editor/',include('froala_editor_views.urls')),
        path('search/', search_views.search, name='search'),
        path('courses/', include('courses.urls')),
        path('feed/', include('feed.urls')),
        path('news/', include('news.urls')),
        path('videos/', include('videos.urls')),
        path('user/', include('users.urls')),
        path('updates/', include('updates.urls')),
        path('stats/', include('stats.urls')),
        path('registration/', include('registration.urls')),
 
        # For anything not caught by a more specific rule above, hand over to
        # Wagtail's page serving mechanism. This should be the last pattern in
        # the list:
        
        path('', include(wagtail_urls)),

        # Alternatively, if you want Wagtail pages to be served from a subpath
        # of your site, rather than the site root:
        #    url(r'^pages/', include(wagtail_urls)),
    ]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
