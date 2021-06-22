from rest_framework import serializers

from .models import Event

class EventSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    pdate = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_banner(self, obj):
        return obj.get_banner

    def get_pdate(self, obj):
        
        return obj.pdate

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        model = Event
        fields = ['start', 'end', 'title', 'body', 'banner', 'pdate', 'url']