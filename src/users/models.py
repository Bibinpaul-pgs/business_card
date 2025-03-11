from firebase.models import AbstractFirebaseUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from firebase_admin import auth
from django.db import models
import random

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