from rest_framework import serializers

from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    countries = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.url

    def get_banner(self, obj):
        return obj.get_banner

    def get_session(self, obj):
        print(obj.next_session)
        return obj.next_session

    def get_price(self, obj):
        return [obj.price.currency, obj.price.amount]

    def get_countries(self, obj):
        try:
            return [str(x).lower() for x in obj.countries if x != 'ON']
        except:
            return ''

    class Meta:
        model = Course
        fields = ['title', 'body', 'price', 'description',
                  'url', 'banner', 'session', 'countries']
