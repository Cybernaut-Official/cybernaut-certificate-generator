from django.db import models

class EmailCredentials(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} ({'Active' if self.active else 'Inactive'})"
