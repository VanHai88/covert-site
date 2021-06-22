from rest_framework import serializers

from .models import Topic

class TopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        fields = ['created', 'subject', 'slug', 'posts_count', 'id',
                  'views_count', 'forum', 'poster', 'first_post', 'uuid', 'tags']
        depth = 1