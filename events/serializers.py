from .models import Event
from rest_framework.serializers import ModelSerializer, SerializerMethodField

class EventSerializer(ModelSerializer):
    thumbnail = SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'title', 'happening_when', 'thumbnail',
            'event_type', 'tag', 'level', 'created_when'
        ]

    # extract the link of image and pass to serializer
    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return ''