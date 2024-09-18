from django.urls import path
from trainings.API.views import training


urlpatterns = [
    path('createtraining/', training.CreateTraining.as_view(), name='create-training'),
    path('readtrainings/', training.ReadTrainings.as_view(), name='read-trainings'),
    path('updatetraining/<int:pk>', training.UpdateTraining.as_view(), name='update-training'),
    path('deletetraining/<int:pk>', training.DestroyTraining.as_view(), name='delete-training'),
]