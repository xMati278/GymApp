from django.urls import path
from trainings.API.views import private_exercise

urlpatterns = [
    path('bodyparts/', private_exercise.GetAllBodyParts.as_view(), name='read-all-body-parts'),
    path('createexercises/', private_exercise.CreatePrivateExercise.as_view(), name='create-exercise'),
    path('exercises/public/', private_exercise.ReadPublicExercises.as_view(), name='read-public-exercises'),
    path('exercises/private/', private_exercise.ReadPrivateExercises.as_view(), name='read-private-exercises'),
    path('updateexercises/<int:pk>', private_exercise.UpdatePrivateExercise.as_view(), name='update-private-exercise'),
    path('deleteexercises/<int:pk>', private_exercise.DeletePrivateExercise.as_view(), name='delete-exercise'),
]