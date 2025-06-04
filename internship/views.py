import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InternUploadForm
from .models import Intern, Internship, InternshipBatch, InternshipRole, InternshipCertificateTemplate
from .serializers import InternshipCertificateTemplateSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .forms import TemplateUploadForm

class InternshipTemplateViewSet(viewsets.ModelViewSet):
    queryset = InternshipCertificateTemplate.objects.all()
    serializer_class = InternshipCertificateTemplateSerializer
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    @action(detail=False, methods=["post"], url_path="upload")
    def upload_template(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Template uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Get all internships
def api_internships(request):
    internships = Internship.objects.all().values("id", "name", "year")
    return JsonResponse(list(internships), safe=False)

# Get batches by internship_id
def api_batches(request):
    internship_id = request.GET.get("internship_id")
    batches = InternshipBatch.objects.filter(internship_id=internship_id).values("id", "month", "name")
    return JsonResponse(list(batches), safe=False)

# Get roles by batch_id
def api_roles(request):
    batch_id = request.GET.get("batch_id")
    roles = InternshipRole.objects.filter(batch_id=batch_id).values("id", "title")
    return JsonResponse(list(roles), safe=False)

@csrf_exempt
def upload_interns(request, role_id):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file uploaded."}, status=400)

        try:
            df = pd.read_excel(file)

            required_columns = {"intern_id", "name", "email"}
            if not required_columns.issubset(df.columns):
                return JsonResponse({"error": f"Missing required columns: {required_columns}"}, status=400)

            for _, row in df.iterrows():
                Intern.objects.update_or_create(
                    intern_id=row["intern_id"],
                    defaults={
                        "name": row["name"],
                        "email": row["email"],
                        "internship_role_id": role_id,
                    },
                )

            return JsonResponse({"success": "Intern data uploaded successfully."})

        except Exception as e:
            return JsonResponse({"error": f"Error processing file: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def upload_interns_page(request):
    return render(request, "upload_interns.html") 

def template_upload_page(request):
    roles = InternshipRole.objects.select_related("batch__internship").all()
    return render(request, "template_upload.html", {"roles": roles})

@csrf_exempt
def upload_template(request, role_id):
    if request.method == "POST":
        try:
            internship_role = InternshipRole.objects.get(id=role_id)
        except InternshipRole.DoesNotExist:
            return JsonResponse({"success": False, "error": "Internship role not found"}, status=404)

        form = TemplateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            # Set foreign keys explicitly for consistency
            template.internship_role = internship_role
            template.batch = internship_role.batch
            template.internship = internship_role.batch.internship
            template.save()
            return JsonResponse({"success": True, "message": "Template uploaded successfully"})
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    return JsonResponse({"error": "Invalid method"}, status=405)

import traceback
from django.http import JsonResponse
from .models import InternshipCertificateTemplate

def api_templates(request):
    try:
        templates = InternshipCertificateTemplate.objects.select_related(
            "internship", "batch", "internship_role"
        ).all()

        data = [
            {
                "id": t.id,
                "internship": t.internship.name if t.internship else "",
                "batch": f"{t.batch.month} {t.batch.name}" if t.batch else "",
                "role": t.internship_role.title if t.internship_role else "",
                "file_url": t.template_file.url if t.template_file else "",
            }
            for t in templates
        ]
        return JsonResponse({"success": True, "templates": data})
    except Exception as e:
        print("Error in api_templates:", e)
        traceback.print_exc()
        return JsonResponse({"success": False, "error": str(e)}, status=500)

def manage_templates_page(request):
    # Just render the HTML page. The data loads via JS fetch from /api/templates/
    return render(request, "view_templates.html")