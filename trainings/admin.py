from django.contrib import admin
from .models import BodyPart, Exercise, UserTrainingPlans, Training, Category, TrainingRecord, TrainingExercise, TrainingPlanExerciseInfo
# Register your models here.

admin.site.register(BodyPart)


class AdminUserTrainingPlans(admin.ModelAdmin):
    list_display = [
        'pk', 'name'
    ]


admin.site.register(Training)
admin.site.register(TrainingRecord)
admin.site.register(Category)
admin.site.register(TrainingExercise)
admin.site.register(TrainingPlanExerciseInfo)


class AdminExercise(admin.ModelAdmin):
    list_display = [
        'pk', 'name', 'user', 'public'
    ]

admin.site.register(Exercise, AdminExercise)
admin.site.register(UserTrainingPlans, AdminUserTrainingPlans)