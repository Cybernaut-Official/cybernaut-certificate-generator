from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from .models import Student
from .serializers import StudentSerializer,StudentUploadSerializer
from .utils import process_student_excel
from programs.models import Course
from .utils import generate_certificate,process_student_excel
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny

@method_decorator(csrf_exempt, name='dispatch')
class UploadStudentsView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]  # Allow all users to access this endpoint
    authentication_classes = []  # Disable authentication checks
    def post(self, request, course_id):
        serializer = StudentUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file = serializer.validated_data["file"]
            response_data = process_student_excel(file, course_id)

            if not isinstance(response_data, dict):
                response_data = {"error": "Unexpected response format from file processing."}

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.all()
        program_id = self.request.query_params.get("program")
        batch_id = self.request.query_params.get("batch")
        course_id = self.request.query_params.get("course")

        if program_id:
            queryset = queryset.filter(course__batch__program_id=program_id)
        if batch_id:
            queryset = queryset.filter(course__batch_id=batch_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset
        
class StudentUploadViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]

    def create(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        result = process_student_excel(file, course.id)
        return Response(result, status=status.HTTP_201_CREATED if "success" in result else status.HTTP_400_BAD_REQUEST)

# class GenerateCertificateView(APIView):
#     def post(self, request, student_id):
#         print(f"Generating certificate for student {student_id}")  # ✅ Debugging Log
#         result = generate_certificate(student_id)
#         return Response({"message": "Certificate generated successfully!", "pdf_path": result}, status=status.HTTP_200_OK)

class GenerateCertificateView(APIView):
    def post(self, request, student_id):
        print(f"🔹 Generating certificate for student {student_id}")  # ✅ Debugging Log

        result = generate_certificate(student_id)  # Call the function

        if "error" in result:
            return Response({"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "message": "Certificate generated successfully",
                "pdf_path": result.get("pdf_path"),
                "result": result.get("success"),
            },
            status=status.HTTP_200_OK
        )
