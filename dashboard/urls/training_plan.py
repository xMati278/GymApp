from django.urls import path
from dashboard.views import training_plan as training_plan

urlpatterns = [
    path('training_plans/', training_plan.ReadTrainingPlans.as_view(), name='training_plans'),
    path('create_training_plan/', training_plan.CreateTrainingPlans.as_view(), name='create_training_plan'),
    path('training_plan/<int:pk>', training_plan.TrainingPlanDetailView.as_view(), name='training_plan_detail'),
    path('training_plan/edit/<int:pk>', training_plan.TrainingPlanEditView.as_view(), name='training_plan_edit'),
    path('training_plans/delete/<int:pk>/', training_plan.DeleteTrainingPlanView.as_view(), name='delete_training_plan'),
    path('training_plans_delete_exercise/<int:pk>/', training_plan.DeleteExerciseFromPlanView.as_view(), name='delete_exercise_from_plan'),
    path('training_plan/<int:pk>/active/', training_plan.ActiveTrainingPlanView.as_view(), name='training_plan_active'),
    path('add_training_exercise/', training_plan.add_training_exercise, name='add_training_exercise'),
]
