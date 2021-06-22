from rest_framework import serializers

from .models import ToolsResources


class ToolsResourcesSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_type_display()

    def get_banner(self, obj):
        return obj.get_banner

    class Meta:
        model = ToolsResources
        fields = ['description', 'name', 'title',
                  'banner', 'type', 'url_address']
