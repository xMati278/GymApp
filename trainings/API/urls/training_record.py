from django.urls import path
from trainings.API.views import training_record

urlpatterns = [
    path('createtrainingrecord/', training_record.CreateTrainingRecord.as_view(), name='create-training-record'),
    path('readtrainingrecord/', training_record.ReadTrainingRecord.as_view(), name='read-training-record'),
    path('updatetrainingrecord/<int:pk>', training_record.UpdateTrainingRecord.as_view(), name='update-training-record'),
    path('deletetrainingrecord/<int:pk>', training_record.DestroyTrainingRecord.as_view(), name='delete-training-record'),
]