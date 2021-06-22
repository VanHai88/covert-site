from rest_framework import serializers

from users.serializers import UserSerializer

from blog.models import BlogPage

class BlogSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    author = UserSerializer()
    categories = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_banner(self, obj):
        return obj.get_banner

    def get_categories(self, obj):
        try:
            return obj.cat_parsed
        except:
            return ''

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        model = BlogPage
        fields = ['body', 'title', 'date', 'banner', 'author', 'categories', 'url']
        depth = 1