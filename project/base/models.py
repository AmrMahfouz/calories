from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from provider.oauth2.models import Client


PROJECT_URL = getattr(settings, 'PROJECT_URL', 'http://localhost')


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
    expected_calories = models.PositiveIntegerField(blank=True, null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


def create_api_key(sender, instance, created, **kwargs):
    if created:
        c = Client(user=instance, name="Calories app client", client_type=1, url=PROJECT_URL)
        c.save()


models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(create_user_profile, sender=User)
