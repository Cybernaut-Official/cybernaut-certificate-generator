from django.db import models

def internship_certificate_upload_path(instance, filename):
    """
    Store certificate as 'certificates/internship_id/batch_id/role_id/intern_id.pdf'
    """
    intern = instance.intern
    role = intern.internship_role
    batch = role.batch
    internship = batch.internship

    return f"certificates/{internship.id}/{batch.id}/{role.id}/{intern.intern_id}.pdf"


class Internship(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ("name", "year")

    def __str__(self):
        return f"{self.name} ({self.year})"


class InternshipBatch(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name="batches")
    month = models.CharField(max_length=20)  # e.g., "January"
    name = models.CharField(max_length=50)   # e.g., "Batch A", "B1"

    class Meta:
        unique_together = ("internship", "month", "name")

    def __str__(self):
        return f"{self.internship.name} - {self.month} {self.name}"


class InternshipRole(models.Model):
    batch = models.ForeignKey(InternshipBatch, on_delete=models.CASCADE, related_name="roles")
    title = models.CharField(max_length=100)  # e.g., "Full Stack Developer"

    class Meta:
        unique_together = ("batch", "title")

    def __str__(self):
        return f"{self.batch} - {self.title}"


class Intern(models.Model):
    intern_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    internship_role = models.ForeignKey(InternshipRole, on_delete=models.CASCADE, related_name="interns")

    @property
    def batch(self):
        return self.internship_role.batch

    @property
    def internship(self):
        return self.internship_role.batch.internship

    @property
    def program_year(self):
        return self.internship.year

    def __str__(self):
        return f"{self.name} ({self.intern_id}) - {self.internship_role}"


class Certificate(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, related_name="certificates")
    generated_on = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to=internship_certificate_upload_path, null=True, blank=True)

    # Store static copy of internship duration (snapshot at time of generation)
    internship_start_date = models.DateField()
    internship_end_date = models.DateField()

    class Meta:
        unique_together = ("intern", "certificate_file")

    @property
    def internship(self):
        return self.intern.internship

    @property
    def batch(self):
        return self.intern.batch

    @property
    def role(self):
        return self.intern.internship_role

    @property
    def certificate_status(self):
        return "sent" if self.certificate_file else "not_sent"

    def __str__(self):
        return f"Certificate for {self.intern.name} - {self.role.title} ({self.internship.year})"


def internship_template_upload_path(instance, filename):
    """
    Store under 'internship_templates/internship_id/batch_id/role_id/filename.ext'
    """
    internship_id = instance.internship.id
    batch_id = instance.batch.id
    role_id = instance.internship_role.id

    return f"internship_templates/{internship_id}/{batch_id}/{role_id}/{filename}"


class InternshipCertificateTemplate(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.PROTECT, related_name='certificate_templates', null=True, blank=True)
    batch = models.ForeignKey(InternshipBatch, on_delete=models.PROTECT, related_name='certificate_templates', null=True, blank=True)
    internship_role = models.ForeignKey(InternshipRole, on_delete=models.PROTECT, related_name='certificate_templates', null=True, blank=True)
    template_file = models.FileField(upload_to=internship_template_upload_path)

    class Meta:
        unique_together = ("internship_role", "template_file")

    def __str__(self):
        return f"Template: {self.internship} - {self.batch} - {self.internship_role.title}"
