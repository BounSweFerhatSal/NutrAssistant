from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# We are aiming to creat a new Profile for each new user automatically :
# this receiver decorator -@receiver- makes this function a "receiver" for a signal ( post_save signal)  sent by "new user creation progress"
# when we receive this sgnal we just do whatever we want :
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # to create a new profile record  succesfully porfile model must allow nulls or has default values
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
