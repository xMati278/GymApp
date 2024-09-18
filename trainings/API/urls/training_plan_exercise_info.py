from django.urls import path
from trainings.API.views import training_plan_exercise_info


urlpatterns = [
    path('createtrainingplanexerciseinfo/', training_plan_exercise_info.CreateTrainingPlanExerciseInfo.as_view(),
         name='create-training-plan-exercise-info'),
    path('readtrainingplanexerciseinfo/', training_plan_exercise_info.ReadTrainingPlanExerciseInfo.as_view(),
         name='read-training-plan-exercise-info'),
    path('updatetrainingplanexerciseinfo/<int:pk>', training_plan_exercise_info.UpdateTrainingPlanExerciseInfo.as_view(),
         name='update-training-plan-exercise-info'),
    path('deletetrainingplanexerciseinfo/<int:pk>', training_plan_exercise_info.DestroyTrainingPlanExerciseInfo.as_view(),
         name='destroy-training-plan-exercise-info'),
]