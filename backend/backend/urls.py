
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_url_patterns = [path('users', include('user.urls')), path('', include('account.urls'))]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="payhere API",
        default_version='v1',
        description="payhere",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^user/', include('user.urls')),
    re_path(r'^account/', include('account.urls')),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('s/', include('shortener.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
