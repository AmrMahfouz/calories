from django.contrib import admin
from .models import Meal


class MealAdmin(admin.ModelAdmin):
    pass

admin.register(Meal, MealAdmin)
