from django.contrib import admin
from .models import BodyPart, Exercise, UserTrainingPlans, Training, Category, TrainingRecord
# Register your models here.

admin.site.register(BodyPart)
admin.site.register(Exercise)
admin.site.register(UserTrainingPlans)
admin.site.register(Training)
admin.site.register(TrainingRecord)
admin.site.register(Category)
