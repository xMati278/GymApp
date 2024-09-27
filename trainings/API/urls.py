from django.urls import path
from trainings.API.views import (calculator, exercise, training_exercise, training_plan_exercise_info,
                                 training_record, training, user_training_plan)

urlpatterns = [
    #CALCULATOR
    path('1rm/', calculator.Calculate1RM.as_view(), name='calculate-1rm'),
    path('wilks/', calculator.CalculateWilks.as_view(), name='calculate-wilks'),
    path('dots/', calculator.CalculateDots.as_view(), name='calculate-dots'),
    path('ipfgl/', calculator.CalculateIpfGl.as_view(), name='calculate-ipf-gl'),
    path('total/', calculator.CalculateTotal.as_view(), name='calculate-total'),

    #EXERCISE
    path('body-parts/', exercise.GetAllBodyParts.as_view(), name='api-read-all-body-parts'),
    path('exercises/', exercise.ListCreateExerciseApiVIew.as_view(), name='api-exercises'),
    path('exercise/edit/<int:pk>', exercise.UpdateDestroyExerciseApiView.as_view(), name='api-edit-exercise'),

    #TRAINING EXERCISE
    path('training_exercises/', training_exercise.ListCreateTrainingExercisesApiView.as_view(), name='api-training-exercises'),
    path('training_exercise/edit/<int:pk>', training_exercise.UpdateDestroyTrainingExerciseApiView.as_view(), name='api-edit-training-exercise'),

    #TRAINING PLAN EXERCISE INFO
    path('training_plan_exercises_info/', training_plan_exercise_info.ListCreateTrainingPlanExerciseInfoApiView.as_view(),
         name='api-training-plan-exercise-info'),
    path('training_plan_exercise_info/edit/<int:pk>', training_plan_exercise_info.UpdateDestroyTrainingPlanExerciseInfoApiView.as_view(),
         name='api-edit-training-plan-exercise-info'),

    #TRAINING RECORD
    path('createtrainingrecord/', training_record.CreateTrainingRecord.as_view(), name='create-training-record'),
    path('readtrainingrecord/', training_record.ReadTrainingRecord.as_view(), name='read-training-record'),
    path('updatetrainingrecord/<int:pk>', training_record.UpdateTrainingRecord.as_view(),
         name='update-training-record'),
    path('deletetrainingrecord/<int:pk>', training_record.DestroyTrainingRecord.as_view(),
         name='delete-training-record'),

    #TRAININGS
    path('trainings/', training.ListCreateTrainingsApiView.as_view(), name='api-trainings'),
    path('trainings/edit/<int:pk>', training.UpdateDestroyTrainingApiView.as_view(), name='api-trainings-edit'),

    #USER TRAINING PLAN
    path('createusertrainingplan/', user_training_plan.CreateUserTrainingPlan.as_view(),
         name='create-user-training-plan'),
    path('readusertrainingplans/', user_training_plan.ReadUserTrainingPlans.as_view(), name='read-user-training-plans'),
    path('updateusertrainingplan/<int:pk>', user_training_plan.UpdateUserTrainingPlan.as_view(),
         name='update-user-training-plan'),
    path('deleteusertrainingplan/<int:pk>', user_training_plan.DeleteUserTrainingPlan.as_view(),
         name='delete-user-training-plan'),
]
