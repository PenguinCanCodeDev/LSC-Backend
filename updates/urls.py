from django.urls import path
from .views import get_updates

urlpatterns = [
    path('', get_updates, name='get_updates'),
]