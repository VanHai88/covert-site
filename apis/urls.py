from rest_framework.routers import DefaultRouter

from blog.api import BlogViewSet
from courses.api import CourseViewSet
from videos.api import VideoViewSet
from events.api import EventViewSet
from tools_resources.api import ToolsResourceViewSet
from machina.apps.forum_conversation.api import TopicViewSet


router = DefaultRouter()
router.register(prefix=r'topics', viewset=TopicViewSet)
router.register(prefix=r'articles', viewset=BlogViewSet)
router.register(prefix=r'courses', viewset=CourseViewSet)
router.register(prefix=r'tools-resources', viewset=ToolsResourceViewSet)
router.register(prefix=r'events', viewset=EventViewSet)
router.register(prefix=r'videos', viewset=VideoViewSet)

urlpatterns = router.urls
