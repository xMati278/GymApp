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
    path('exercises/edit/<int:pk>', exercise.UpdateDestroyExerciseApiView.as_view(), name='api-edit-exercise'),

    #TRAINING EXERCISE
    path('training_exercises/', training_exercise.ListCreateTrainingExercisesApiView.as_view(), name='api-training-exercises'),
    path('training_exercises/edit/<int:pk>', training_exercise.UpdateDestroyTrainingExerciseApiView.as_view(), name='api-edit-training-exercise'),

    #TRAINING PLAN EXERCISE INFO
    path('training_plan_exercises_info/', training_plan_exercise_info.ListCreateTrainingPlanExerciseInfoApiView.as_view(),
         name='api-training-plan-exercise-info'),
    path('training_plan_exercises_info/edit/<int:pk>', training_plan_exercise_info.UpdateDestroyTrainingPlanExerciseInfoApiView.as_view(),
         name='api-edit-training-plan-exercise-info'),

    #TRAINING RECORD
    path('training_records/', training_record.ListCreateTrainingRecordsApiView.as_view(), name='api-training-records'),
    path('training_records/edit/<int:pk>', training_record.UpdateDestroyTrainingRecordApiView.as_view(), name='api-edit-training-record'),

    #TRAININGS
    path('trainings/', training.ListCreateTrainingsApiView.as_view(), name='api-trainings'),
    path('trainings/edit/<int:pk>', training.UpdateDestroyTrainingApiView.as_view(), name='api-trainings-edit'),

    #USER TRAINING PLAN
    path('user_training_plans/', user_training_plan.ListCreateUserTrainingPlanApiView.as_view(), name='api-user-training-plan'),
    path('user_training_plans/edit/<int:pk>', user_training_plan.UpdateDestroyUserTrainingPlanApiView.as_view(), name='api-edit-user-training-plan'),
    # path('createusertrainingplan/', user_training_plan.CreateUserTrainingPlan.as_view(),
    #      name='create-user-training-plan'),
    # path('readusertrainingplans/', user_training_plan.ReadUserTrainingPlans.as_view(), name='read-user-training-plans'),
    # path('updateusertrainingplan/<int:pk>', user_training_plan.UpdateUserTrainingPlan.as_view(),
    #      name='update-user-training-plan'),
    # path('deleteusertrainingplan/<int:pk>', user_training_plan.DeleteUserTrainingPlan.as_view(),
    #      name='delete-user-training-plan'),
]
