from django.urls import path
from django.contrib.auth.views import LogoutView
from dashboard.views import auth as auth

urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
