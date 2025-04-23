from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, BatchViewSet, CourseViewSet

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = router.urls
