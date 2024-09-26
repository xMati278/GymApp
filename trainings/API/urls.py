from django.urls import path
from trainings.API.views import (calculator, private_exercise, training_exercise, training_plan_exercise_info,
                                 training_record, training, user_training_plan)

urlpatterns = [
    #CALCULATOR
    path('1rm/', calculator.Calculate1RM.as_view(), name='calculate-1rm'),
    path('wilks/', calculator.CalculateWilks.as_view(), name='calculate-wilks'),
    path('dots/', calculator.CalculateDots.as_view(), name='calculate-dots'),
    path('ipfgl/', calculator.CalculateIpfGl.as_view(), name='calculate-ipf-gl'),
    path('total/', calculator.CalculateTotal.as_view(), name='calculate-total'),

    #EXERCISE
    path('body-parts/', private_exercise.GetAllBodyParts.as_view(), name='read-all-body-parts'),
    path('createexercises/', private_exercise.CreatePrivateExercise.as_view(), name='create-exercise'),
    # exercises definuje CI POST
    path('exercises/public/', private_exercise.ReadPublicExercises.as_view(), name='read-public-exercises'),
    path('exercises/private/', private_exercise.ReadPrivateExercises.as_view(), name='read-private-exercises'),
    # path('exercises/private/', private_exercise.ListCreatePrivateExercisesAPIView.as_view(), ...) # exercises/private GET (list), POST (create), DELETE (method not allowd 405)
    path('updateexercises/<int:pk>', private_exercise.UpdatePrivateExercise.as_view(), name='update-private-exercise'),
    # exercises/<int:pk>/private
    path('deleteexercises/<int:pk>', private_exercise.DeletePrivateExercise.as_view(), name='delete-exercise'),
    # exercises/<int:pk>/private

    #TRAINING EXERCISE
    path('createtrainingexercise/', training_exercise.CreateTrainingExercise.as_view(),
         name='create-training-exercise'),
    path('readtrainingexercise/', training_exercise.ReadTrainingExercise.as_view(), name='read-training-exercise'),
    path('updatetrainingexercise/<int:pk>', training_exercise.UpdateTrainingExercise.as_view(),
         name='update-training-exercise'),
    path('deletetrainingexercise/<int:pk>', training_exercise.DestroyTrainingExercise.as_view(),
         name='delete-training-exercise'),

    #TRAINING PLAN EXERCISE INFO
    path('createtrainingplanexerciseinfo/', training_plan_exercise_info.CreateTrainingPlanExerciseInfo.as_view(),
         name='create-training-plan-exercise-info'),
    path('readtrainingplanexerciseinfo/', training_plan_exercise_info.ReadTrainingPlanExerciseInfo.as_view(),
         name='read-training-plan-exercise-info'),
    path('updatetrainingplanexerciseinfo/<int:pk>',
         training_plan_exercise_info.UpdateTrainingPlanExerciseInfo.as_view(),
         name='update-training-plan-exercise-info'),
    path('deletetrainingplanexerciseinfo/<int:pk>',
         training_plan_exercise_info.DestroyTrainingPlanExerciseInfo.as_view(),
         name='destroy-training-plan-exercise-info'),

    #TRAINING RECORD
    path('createtrainingrecord/', training_record.CreateTrainingRecord.as_view(), name='create-training-record'),
    path('readtrainingrecord/', training_record.ReadTrainingRecord.as_view(), name='read-training-record'),
    path('updatetrainingrecord/<int:pk>', training_record.UpdateTrainingRecord.as_view(),
         name='update-training-record'),
    path('deletetrainingrecord/<int:pk>', training_record.DestroyTrainingRecord.as_view(),
         name='delete-training-record'),

    #TRAININGS
    path('createtraining/', training.CreateTraining.as_view(), name='create-training'),
    path('readtrainings/', training.ReadTrainings.as_view(), name='read-trainings'),
    path('updatetraining/<int:pk>', training.UpdateTraining.as_view(), name='update-training'),
    path('deletetraining/<int:pk>', training.DestroyTraining.as_view(), name='delete-training'),

    #USER TRAINING PLAN
    path('createusertrainingplan/', user_training_plan.CreateUserTrainingPlan.as_view(),
         name='create-user-training-plan'),
    path('readusertrainingplans/', user_training_plan.ReadUserTrainingPlans.as_view(), name='read-user-training-plans'),
    path('updateusertrainingplan/<int:pk>', user_training_plan.UpdateUserTrainingPlan.as_view(),
         name='update-user-training-plan'),
    path('deleteusertrainingplan/<int:pk>', user_training_plan.DeleteUserTrainingPlan.as_view(),
         name='delete-user-training-plan'),
]
