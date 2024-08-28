from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    #DASHBOARD PAGES

    path('calculator/', views.CalculatorView.as_view(), name='calculator'),
    path('calculator_result/', views.CalculatorResultView.as_view(), name='calculator_result'),


    path('training_plans/', views.training_plans_view, name='training_plans'),


    path('history/', views.history_view, name='history'),


    path('exercises/', views.ExercisesView.as_view(), name='exercises'),
    path('exercises/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercise/<int:pk>/edit/', views.ExerciseEditView.as_view(), name='exercise_edit'),
    path('exercise/add/', views.AddExerciseView.as_view(), name='add_exercise'),
    path('exercise/<int:pk>/delete', views.DeleteExerciseView.as_view(), name='delete_exercise'),


    path('records/', views.records_view, name='records'),
    path('', RedirectView.as_view(pattern_name='training_plans', permanent=False), name='home'),
]