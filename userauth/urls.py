from django.urls import path
from .views import (
    home, get_user_info,
    register_user, login_user,
    refresh_token, logout_user
)

urlpatterns = [
    path('', home),

    path('my-user-info/', get_user_info),

    # auth 
    path('auth/register/', register_user),
    path('auth/token/', login_user),
    path('auth/token/refresh/', refresh_token),
    path('auth/logout/', logout_user),
]