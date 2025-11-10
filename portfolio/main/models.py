from django.db import models

class Experience(models.Model):
    title = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='experiences/', null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role} at {self.organization}"

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/', null=True, blank=True)
    category = models.CharField(max_length=100, choices=[
        ('license', 'License & Certification'),
        ('competition', 'Competition & Award'),
    ], default='competition')

    def __str__(self):
        return self.title
