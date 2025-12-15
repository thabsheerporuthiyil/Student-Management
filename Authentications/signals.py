from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import User, StudentProfile
from .models import generate_roll_number


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "student":
        StudentProfile.objects.create(
            user=instance,
            roll_number=generate_roll_number(),
            year_of_admission=now().year
        )

