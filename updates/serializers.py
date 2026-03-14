from rest_framework.serializers import ModelSerializer
from .models import Update


class UpdateSerializer(ModelSerializer):
    class Meta:
        model = Update
        fields = ['title', 'type', 'tag', 'happening_when', 'link']