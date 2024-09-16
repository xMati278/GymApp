from django.urls import path
from dashboard.views import exercise as exercise

urlpatterns = [
    path('exercises/', exercise.ExercisesView.as_view(), name='exercises'),
    path('exercises/<int:pk>/', exercise.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercise/<int:pk>/edit/', exercise.ExerciseEditView.as_view(), name='exercise_edit'),
    path('exercise/create/', exercise.CreateExerciseView.as_view(), name='create_exercise'),
    path('exercise/<int:pk>/delete/', exercise.DeleteExerciseView.as_view(), name='delete_exercise'),
]
