from django.urls import path
from .views import *

urlpatterns = [
    path('tag/<int:tag>/', tag_view, name="tag"),
    path('category/<int:category>/feed/$', LatestCategoryFeed(), name="category_feed"),
    path('category/<int:category>/', category_view, name="category"),
    path('author/<int:author>/', author_view, name="author"),
    path('<slug:blog_slug>/rss.*/',
        LatestEntriesFeed(),
        name="latest_entries_feed"),
    path('<slug:blog_slug>/atom.*/',
        LatestEntriesFeedAtom(),
        name="latest_entries_feed_atom"),
]