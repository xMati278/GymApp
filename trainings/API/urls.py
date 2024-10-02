from django.urls import path, include
from trainings.API.views import (user_training_plan)
from rest_framework.routers import DefaultRouter
from trainings.API.views import calculator, exercise, training, training_exercise, training_plan_exercise_info, training_record


router = DefaultRouter()
router.register(r'exercises', exercise.ExerciseViewSet, basename='api-exercises')
router.register(r'trainings', training.TrainingViewSet, basename='api-trainings')
router.register(r'training-exercises', training_exercise.TrainingExerciseViewSet, basename='api-training-exercises')
router.register(r'training-plan-exercise-info', training_plan_exercise_info.TrainingPlanExerciseInfoViewSet,
                basename='api-training-plan-exercise-info')
router.register(r'training-records', training_record.TrainingRecordViewSet, basename='api-training-records')

urlpatterns = [
    #CALCULATOR
    path('1rm/', calculator.Calculate1RM.as_view(), name='calculate-1rm'),
    path('wilks/', calculator.CalculateWilks.as_view(), name='calculate-wilks'),
    path('dots/', calculator.CalculateDots.as_view(), name='calculate-dots'),
    path('ipfgl/', calculator.CalculateIpfGl.as_view(), name='calculate-ipf-gl'),
    path('total/', calculator.CalculateTotal.as_view(), name='calculate-total'),

    path('body-parts/', exercise.GetAllBodyParts.as_view(), name='api-read-all-body-parts'),
    path('', include(router.urls)),

    #USER TRAINING PLAN
    path('user-training-plans/', user_training_plan.ListCreateUserTrainingPlanApiView.as_view(), name='api-user-training-plan'),
    path('user-training-plans/<int:pk>', user_training_plan.UpdateDestroyUserTrainingPlanApiView.as_view(), name='api-edit-user-training-plan'),
]
