from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Lopl-ecommerce",
        default_version='v1',
        description="Lopl-ecommerce Backend Server",
        contact=openapi.Contact(email="hell@princewilldev.com"),
        license=openapi.License(name="Protected"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/auth/', include('auth_api_v1.urls')),
    # path('api/v1/product/', include('products_api_v1.urls')),

    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

