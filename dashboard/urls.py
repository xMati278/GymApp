from django.urls import path
from django.contrib.auth.views import LogoutView
from dashboard.views import auth, calculator, exercise, history, record, training_plan

urlpatterns = [
    #AUTH
    path('login/', auth.LoginView.as_view(), name='login'),
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    #CALCULATOR
    path('calculator/', calculator.CalculatorView.as_view(), name='calculator'),
    path('calculator_result/', calculator.CalculatorResultView.as_view(), name='calculator_result'),

    #EXERCISE
    path('exercises/', exercise.ExercisesView.as_view(), name='exercises'),
    path('exercises/<int:pk>/', exercise.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercise/<int:pk>/edit/', exercise.ExerciseEditView.as_view(), name='exercise_edit'),
    path('exercise/create/', exercise.CreateExerciseView.as_view(), name='create_exercise'),
    path('exercise/<int:pk>/delete/', exercise.DeleteExerciseView.as_view(), name='delete_exercise'),

    #HISTORY
    path('history/', history.history_view, name='history'),

    #RECORD
    path('records/', record.records_view, name='records'),

    #TRAINING_PLAN
    path('training_plans/', training_plan.ReadTrainingPlans.as_view(), name='training_plans'),
    path('create_training_plan/', training_plan.CreateTrainingPlans.as_view(), name='create_training_plan'),
    path('training_plan/<int:pk>', training_plan.TrainingPlanDetailView.as_view(), name='training_plan_detail'),
    path('training_plan/edit/<int:pk>', training_plan.TrainingPlanEditView.as_view(), name='training_plan_edit'),
    path('training_plans/delete/<int:pk>/', training_plan.DeleteTrainingPlanView.as_view(),
         name='delete_training_plan'),
    path('training_plans_delete_exercise/<int:pk>/', training_plan.DeleteExerciseFromPlanView.as_view(),
         name='delete_exercise_from_plan'),
    path('training_plan/<int:pk>/active/', training_plan.ActiveTrainingPlanView.as_view(), name='training_plan_active'),
    path('add_training_exercise/', training_plan.add_training_exercise, name='add_training_exercise'),
]