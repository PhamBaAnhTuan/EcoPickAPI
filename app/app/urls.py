"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Swagger / OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # App routes
    path("api/roles/", include("role.urls")),
    path("api/users/", include("user.urls")),
    path("api/event/", include("event.urls")),
    path("api/post/", include("post.urls")),
    path("api/report/", include("report.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/badge/", include("badge.urls")),
]
