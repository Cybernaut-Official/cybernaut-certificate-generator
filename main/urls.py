from django.urls import path
from . import views
from .views import UploadStudentsView, get_programs, get_batches, get_courses, get_students_by_course, student_list_page, upload_template_view
from .views import certificate_template_list

urlpatterns = [
    path("", views.home, name="home"),
    path("upload-students/", UploadStudentsView, name="upload_students"),
    path("students/<int:course_id>/", get_students_by_course, name="get_students"),
    path("students/", student_list_page, name="student_list"),
    path("programs/", get_programs, name="get_programs"),
    path("batches/<int:program_id>/", get_batches, name="get_batches"),
    path("courses/<int:batch_id>/", get_courses, name="get_courses"),
    path("students/<int:course_id>/", get_students_by_course, name="get_students"),
    path("students/", student_list_page, name="student_list"),
    path("upload-template/", upload_template_view, name="upload_template"),
    path("certificate-templates/", certificate_template_list, name="certificate-template-list"),

]
