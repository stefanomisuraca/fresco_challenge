"""fresco_project URL Configuration """

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/v1/', include('v1.api_views.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('api-token-auth/', views.obtain_auth_token)
]
