from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from rest_framework import permissions
from post.views import PostViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    info=openapi.Info(
        title='Free Travel',
        default_version='v1',
        description='Hakaton project',
        terms_of_service='http://www.google.com/policies/terms/',
        contact=openapi.Contact(email='test@gmail.com'),
        license=openapi.License(name='BSD License')
    ),
    public=True,
    permission_classes = (permissions.AllowAny, ),
)


router = DefaultRouter()
router.register('posts', PostViewSet)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/accounts/', include('user.urls')),
    path('api/v1/', include('post.urls')),
    path('api/v1/', include(router.urls)),
]
