from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models import Max
from datetime import date

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Course(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    year_of_admission = models.IntegerField(default=date.today().year)
    image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    courses = models.ManyToManyField("Course", blank=True)

    def save(self, *args, **kwargs):
        if not self.roll_number:
            self.roll_number = f"{self.year_of_admission}-{self.user.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


def generate_roll_number():
    last_num = StudentProfile.objects.aggregate(
        max_roll=Max("roll_number")
    )["max_roll"]

    if not last_num:
        return "S0001"

    last_num_int = int(last_num[1:])
    return f"S{last_num_int + 1:04d}"
