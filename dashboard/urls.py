from django.contrib import admin
from django.urls import path, include
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
    path('exercises/', views.exercises_view, name='exercises'),
    path('records/', views.records_view, name='records'),
]