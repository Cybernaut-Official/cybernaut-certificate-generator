from django.http import JsonResponse, HttpResponse
import requests
from students.models import Student
from programs.models import Program, Batch, Course
from django.shortcuts import get_object_or_404, render
from templates.models import CertificateTemplate

def home(request):
    return render(request, "home.html")


def UploadStudentsView(request):
    """Render the student upload form."""
    return render(request, "upload_students.html")

def fetch_programs():
    """Fetch programs from the API."""
    response = requests.get("http://127.0.0.1:8000/api/programs/")
    return response.json() if response.status_code == 200 else []

def fetch_batches(program_id):
    """Fetch batches for a selected program."""
    response = requests.get(f"http://127.0.0.1:8000/api/batches/?program={program_id}")
    return response.json() if response.status_code == 200 else []

def fetch_courses(batch_id):
    """Fetch courses for a selected batch."""
    response = requests.get(f"http://127.0.0.1:8000/api/courses/{batch_id}")
    return response.json() if response.status_code == 200 else []





def get_programs(request):
    """Fetch all programs"""
    programs = Program.objects.values("id", "name", "year")
    return JsonResponse(list(programs), safe=False)

def get_batches(request, program_id):
    """Fetch batches for a specific program"""
    batches = Batch.objects.filter(program_id=program_id).values("id", "month", "name")
    return JsonResponse(list(batches), safe=False)

def get_courses(request, batch_id):
    """Fetch courses for a specific batch"""
    courses = Course.objects.filter(batch_id=batch_id).values("id", "name")
    return JsonResponse(list(courses), safe=False)

def get_students_by_course(request, course_id):
    """Fetch students for a specific course."""
    course = get_object_or_404(Course, id=course_id)
    students = Student.objects.filter(course=course).values(
        "id", "name", "email", "batch__name", "certificate_file"
    )
    return JsonResponse(list(students), safe=False)

def student_list_page(request):
    """Render Student List Page."""
    return render(request, "student_list.html")


def upload_template_view(request):
    return render(request, "upload_template.html")

def certificate_template_list(request):
    templates = CertificateTemplate.objects.all()
    
    template_data = []
    for template in templates:
        program_info = template.get_program_and_year()
        template_data.append({
            "id": template.id,
            "program_name": program_info["program_name"],
            "year": program_info["year"],
            "batch_name": template.course.batch.name,
            "course_name": template.course.name,
            "file_url": template.template_file.url if template.template_file else "#"
        })

    return render(request, "manage_templates.html", {"templates": template_data})