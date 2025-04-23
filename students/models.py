from django.db import models
from programs.models import Course

def certificate_upload_path(instance, filename):
    """Store certificates under 'certificates/course_id/student_id.pdf'"""
    return f"media/certificates/{instance.course.id}/{instance.id}.pdf"

class Student(models.Model):
    serial_number = models.CharField(max_length=50)  # Unique per course
    unique_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    final_mark = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="students")
    certificate_file = models.FileField(upload_to=certificate_upload_path, null=True, blank=True)

    class Meta:
        unique_together = ("course", "email", "serial_number")  # Ensures uniqueness per course

    @property
    def batch(self):
        """Retrieve batch dynamically via the course"""
        return self.course.batch

    @property
    def program(self):
        """Retrieve program dynamically via batch"""
        return self.course.batch.program

    @property
    def program_year(self):
        """Retrieve the program year dynamically"""
        return self.program.year
        
    @property
    def certificate_status(self):
        if self.certificate_file:
            return "sent"
        return "not_sent"


    def __str__(self):
        return f"{self.name} - {self.course.name} ({self.program.year})"
