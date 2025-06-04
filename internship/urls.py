from django.urls import path
from . import views

urlpatterns = [
    # Existing API views
    path("internships/", views.api_internships, name="api-internships"),
    path("batches/", views.api_batches, name="api-batches"),
    path("roles/", views.api_roles, name="api-roles"),

    # Intern bulk upload
    path("interns/upload/<int:role_id>/", views.upload_interns, name="upload-interns"),
    path("upload-interns/", views.upload_interns_page, name="upload_interns"),

    # ✅ Template upload and management views
    path("template-upload/", views.template_upload_page, name="template_upload_page"),  # HTML upload form
    path("template-upload/<int:role_id>/", views.upload_template, name="upload_template"),  # Handle file upload POST
    path("interns/templates/", views.api_templates, name="api_templates"),  # Optional: List templates

    path("manage-templates/", views.manage_templates_page, name="manage_templates_page"),

]
