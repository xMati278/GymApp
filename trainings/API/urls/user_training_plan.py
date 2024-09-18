from django.urls import path
from trainings.API.views import user_training_plan

urlpatterns = [
    path('createusertrainingplan/', user_training_plan.CreateUserTrainingPlan.as_view(), name='create-user-training-plan'),
    path('readusertrainingplans/', user_training_plan.ReadUserTrainingPlans.as_view(), name='read-user-training-plans'),
    path('updateusertrainingplan/<int:pk>', user_training_plan.UpdateUserTrainingPlan.as_view(), name='update-user-training-plan'),
    path('deleteusertrainingplan/<int:pk>', user_training_plan.DeleteUserTrainingPlan.as_view(), name='delete-user-training-plan'),
]