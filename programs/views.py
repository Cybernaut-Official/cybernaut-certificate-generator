from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Program, Batch, Course
from .serializers import ProgramSerializer, BatchSerializer, CourseSerializer

class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        """
        Filter programs by year if 'year' parameter is provided.
        """
        queryset = Program.objects.all()
        year = self.request.query_params.get("year")
        if year:
            queryset = queryset.filter(year=year)
        return queryset

    @action(detail=False, methods=["get"])
    def all(self, request):
        """Returns all programs (no filters applied)"""
        programs = Program.objects.all()
        serializer = self.get_serializer(programs, many=True)
        return Response(serializer.data)

class BatchViewSet(viewsets.ModelViewSet):
    serializer_class = BatchSerializer

    def get_queryset(self):
        """
        Return batches filtered by program_id if provided.
        Otherwise, return all batches.
        """
        program_id = self.request.query_params.get("program_id")
        if program_id:
            return Batch.objects.filter(program_id=program_id)
        return Batch.objects.all()  # Fix: Return all instead of `none()`

    @action(detail=False, methods=["get"])
    def all(self, request):
        """Returns all batches (no filters applied)"""
        batches = Batch.objects.all()
        serializer = self.get_serializer(batches, many=True)
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Return courses filtered by batch_id if provided.
        If not, filter by program_id.
        """
        queryset = Course.objects.all()
        batch_id = self.request.query_params.get("batch_id")
        program_id = self.request.query_params.get("program_id")

        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
        elif program_id:
            queryset = queryset.filter(batch__program_id=program_id)

        return queryset

    @action(detail=False, methods=["get"])
    def all(self, request):
        """Returns all courses (no filters applied)"""
        courses = Course.objects.all()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)