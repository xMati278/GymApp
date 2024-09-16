"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('API.urls')),
    path('', include('dashboard.urls.auth')),
    path('', include('dashboard.urls.calculator')),
    path('', include('dashboard.urls.exercise')),
    path('', include('dashboard.urls.history')),
    path('', include('dashboard.urls.record')),
    path('', include('dashboard.urls.training_plan')),

    path('', RedirectView.as_view(pattern_name='training_plans', permanent=False), name='home'),

]
