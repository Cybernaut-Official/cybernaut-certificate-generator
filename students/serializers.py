from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'serial_number', 'unique_id', 'name', 'email', 'phone_number', 'final_mark', 'date', 'certificate_status', 'certificate_file']
    
    def get_certificate_status(self, obj):
        return obj.certificate_status

class StudentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
