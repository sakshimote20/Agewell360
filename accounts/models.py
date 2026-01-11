from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    family_contact = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    is_profile_completed = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # ensure profile exists for existing users
        Profile.objects.get_or_create(user=instance)
