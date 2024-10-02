from django.urls import path, include
from trainings.API.views import (training_plan_exercise_info,
                                 training_record,user_training_plan)
from rest_framework.routers import DefaultRouter
from trainings.API.views import calculator, exercise, training, training_exercise


router = DefaultRouter()
router.register(r'exercises', exercise.ExerciseViewSet, basename='api-exercises')
router.register(r'trainings', training.TrainingViewSet, basename='api-trainings')
router.register(r'training-exercises', training_exercise.TrainingExerciseViewSet, basename='api-training-exercises')


urlpatterns = [
    #CALCULATOR
    path('1rm/', calculator.Calculate1RM.as_view(), name='calculate-1rm'),
    path('wilks/', calculator.CalculateWilks.as_view(), name='calculate-wilks'),
    path('dots/', calculator.CalculateDots.as_view(), name='calculate-dots'),
    path('ipfgl/', calculator.CalculateIpfGl.as_view(), name='calculate-ipf-gl'),
    path('total/', calculator.CalculateTotal.as_view(), name='calculate-total'),

    path('body-parts/', exercise.GetAllBodyParts.as_view(), name='api-read-all-body-parts'),
    path('', include(router.urls)),

    #TRAINING PLAN EXERCISE INFO
    path('training-plan-exercises-info/', training_plan_exercise_info.ListCreateTrainingPlanExerciseInfoApiView.as_view(),
         name='api-training-plan-exercise-info'),
    path('training-plan-exercises-info/<int:pk>', training_plan_exercise_info.UpdateDestroyTrainingPlanExerciseInfoApiView.as_view(),
         name='api-edit-training-plan-exercise-info'),

    #TRAINING RECORD
    path('training-records/', training_record.ListCreateTrainingRecordsApiView.as_view(), name='api-training-records'),
    path('training-records/<int:pk>', training_record.UpdateDestroyTrainingRecordApiView.as_view(), name='api-edit-training-record'),

    #USER TRAINING PLAN
    path('user-training-plans/', user_training_plan.ListCreateUserTrainingPlanApiView.as_view(), name='api-user-training-plan'),
    path('user-training-plans/<int:pk>', user_training_plan.UpdateDestroyUserTrainingPlanApiView.as_view(), name='api-edit-user-training-plan'),
]
