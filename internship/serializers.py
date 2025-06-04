from rest_framework import serializers
from .models import InternshipCertificateTemplate, Internship, InternshipBatch, InternshipRole

class InternshipCertificateTemplateSerializer(serializers.ModelSerializer):
    internship = serializers.SerializerMethodField()
    batch = serializers.SerializerMethodField()
    role_title = serializers.CharField(source="internship_role.title", read_only=True)
    file_url = serializers.SerializerMethodField()

    internship_role = serializers.PrimaryKeyRelatedField(queryset=InternshipRole.objects.all())

    class Meta:
        model = InternshipCertificateTemplate
        fields = [
            "id",
            "internship",
            "batch",
            "role_title",
            "internship_role",
            "template_file",
            "file_url"
        ]

    def get_internship(self, obj):
        return obj.internship.name

    def get_batch(self, obj):
        return f"{obj.batch.month} {obj.batch.name}"

    def get_file_url(self, obj):
        return obj.template_file.url if obj.template_file else None
