from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=255, unique=False)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.year})"


class Batch(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="batches")
    month = models.CharField(max_length=20)  # Example: "January"
    name = models.CharField(max_length=50)   # Example: "B1", "B2"

    class Meta:
        unique_together = ("program", "month", "name")

    def __str__(self):
        return f"{self.program.name} - {self.month} {self.name}"


class Course(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("batch", "name")

    def __str__(self):
        return f"{self.batch} - {self.name} ({self.batch.program.year})"
