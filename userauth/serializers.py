from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password',
            'campus', 'faculty', 'department',
            'matriculation_number', 'user_type'
        ]