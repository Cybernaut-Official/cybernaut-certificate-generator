from django.db import models
from programs.models import Course

def template_upload_path(instance, filename):
    """Store templates under 'certificate_templates/program_id/batch_id/course_id/'"""
    return f"certificate_templates/{instance.course.batch.program.id}/{instance.course.batch.id}/{instance.course.id}/{filename}"

class CertificateTemplate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificate_templates")  # ✅ Changed to ForeignKey
    template_file = models.FileField(upload_to=template_upload_path)

    class Meta:
        unique_together = ["course", "template_file"]  # ✅ Ensures a course can have multiple templates but not duplicate ones

    def __str__(self):
        return f"Template for {self.course.batch.program.name} - {self.course.batch.name} - {self.course.name}"

    def get_program_and_year(self):
        """Returns the program name and year for this template."""
        program = self.course.batch.program
        return {"program_name": program.name, "year": program.year}
