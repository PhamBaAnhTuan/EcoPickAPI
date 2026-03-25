from django.urls import path, include
from report.views import ReportImageViewSet, ReportViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reports', ReportViewSet)
router.register(r'report-images', ReportImageViewSet)

urlpatterns = router.urls