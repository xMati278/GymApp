from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_user, name='logout'),

    #DASHBOARD PAGES
    path('calculator/', views.calculator_view, name='calculator'),
    path('training_plans/', views.training_plans_view, name='training_plans'),
    path('history/', views.history_view, name='history'),
    path('exercises/', views.exercises_view, name='exercises'),
    path('records/', views.records_view, name='records'),
]