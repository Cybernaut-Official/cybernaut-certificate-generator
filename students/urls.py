from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentUploadViewSet, GenerateCertificateView, UploadStudentsView

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')
urlpatterns = [
    path('', include(router.urls)),
    
    path('students/generate-certificate/<int:student_id>/', GenerateCertificateView.as_view()),
    path("students/upload/<int:course_id>/", UploadStudentsView.as_view(), name="upload-students"),

]
