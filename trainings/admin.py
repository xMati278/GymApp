from django.contrib import admin
from .models import BodyPart, Exercise, UserTrainingPlans, Training, Category, TrainingRecord, TrainingExercise
# Register your models here.

admin.site.register(BodyPart)



admin.site.register(UserTrainingPlans)
admin.site.register(Training)
admin.site.register(TrainingRecord)
admin.site.register(Category)
admin.site.register(TrainingExercise)


class AdminExercise(admin.ModelAdmin):
    list_display = [
        'pk', 'name', 'user', 'public'
    ]

admin.site.register(Exercise, AdminExercise)