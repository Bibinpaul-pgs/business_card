from firebase.models import AbstractFirebaseUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from firebase_admin import auth
from django.db import models
import random
from core.models import BaseModel

class User(AbstractFirebaseUser):
    otp = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'



@receiver(pre_save, sender=User)
def add_user_to_firebase(sender, instance, *args, **kwargs):
    if instance.pk is None:
        user = auth.create_user(
            email=instance.email,
            password=instance.password,
            display_name=instance.display_name,
        )


@receiver(post_save, sender=User)
def post_save_user_otp(sender, instance, created, **kwargs):
    if created:
        instance.otp = random.randint(0, 999999)
        instance.save()


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_image = models.FileField(upload_to="user/profile_image", null=True, blank=True)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    designation = models.CharField(max_length=300, null=True, blank=True)
    company_name = models.CharField(max_length=500, help_text='Company/Organisation name', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    location_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)