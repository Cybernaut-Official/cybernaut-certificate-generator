from rest_framework import serializers
from .models import CertificateTemplate, Course

class CertificateTemplateSerializer(serializers.ModelSerializer):
    program = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    batch = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    # ✅ Allow `course` to be written and received as `course_id`
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True
    )

    class Meta:
        model = CertificateTemplate
        fields = ["id", "program", "year", "batch", "course", "template_file", "file_url"]
        extra_kwargs = {"template_file": {"required": True}}  # ✅ Ensure file upload is mandatory

    def get_program(self, obj):
        return obj.course.batch.program.name if obj.course and obj.course.batch.program else None

    def get_year(self, obj):
        return obj.course.batch.program.year if obj.course and obj.course.batch.program else None

    def get_batch(self, obj):
        return obj.course.batch.name if obj.course and obj.course.batch else None

    def get_file_url(self, obj):
        return obj.template_file.url if obj.template_file else None

    def create(self, validated_data):
        """ ✅ Ensure `template_file` is handled properly from request.FILES """
        request = self.context.get("request")
        if request and "template_file" in request.FILES:
            validated_data["template_file"] = request.FILES["template_file"]
        else:
            raise serializers.ValidationError({"template_file": "This field is required."})

        return super().create(validated_data)
