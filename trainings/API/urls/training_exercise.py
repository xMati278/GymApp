from django.urls import path
from trainings.API.views import training_exercise


urlpatterns = [
    path('createtrainingexercise/', training_exercise.CreateTrainingExercise.as_view(), name='create-training-exercise'),
    path('readtrainingexercise/', training_exercise.ReadTrainingExercise.as_view(), name='read-training-exercise'),
    path('updatetrainingexercise/<int:pk>', training_exercise.UpdateTrainingExercise.as_view(), name='update-training-exercise'),
    path('deletetrainingexercise/<int:pk>', training_exercise.DestroyTrainingExercise.as_view(), name='delete-training-exercise'),
]