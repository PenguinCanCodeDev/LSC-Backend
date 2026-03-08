from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="LSC API",
      default_version='v1',
      description="Below, you will find all endpoints and documentation to each of these endpoints",
      contact=openapi.Contact(email="adesolaayodeji53@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url=settings.SWAGGER_DOCS_BASE_URL,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('userauth.urls')),
    path('api/updates/', include('updates.urls')),
    path('api/events/', include('events.urls')),

    # swagger UI
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
