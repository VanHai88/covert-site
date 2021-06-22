from rest_framework import serializers
from .models import VideoPage


class VideoSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_banner(self, obj):
        return obj.get_banner

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        model = VideoPage
        fields = [
            'name',
            'url',
            'banner',
            'description',
        ]
