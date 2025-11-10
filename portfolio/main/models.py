from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    tiktok_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Profile"

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


class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    organization = models.CharField(max_length=200, blank=True)
    focus_area = models.CharField(max_length=120, help_text="e.g., Capital Markets, Leadership")
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} on {self.focus_area}"

    @property
    def initials(self):
        parts = self.name.strip().split()
        if not parts:
            return "??"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return f"{parts[0][0]}{parts[-1][0]}".upper()


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
