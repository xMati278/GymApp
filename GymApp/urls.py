from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView


api_v1 = [
    path('api/v1/', include('accounts.API.urls')),
    path('api/v1/', include('trainings.API.urls')),
    path('api/v1/', include('calculators.API.urls')),
]

web_app = [
    path('', include('dashboard.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='training_plans', permanent=False), name='home'),

]

urlpatterns += api_v1
urlpatterns += web_app