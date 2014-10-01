from django.db import models


class Meal(models.Model):
    user = models.ForeignKey('auth.User')
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    calories = models.PositiveIntegerField()
    text = models.TextField()
