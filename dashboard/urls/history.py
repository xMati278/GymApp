from django.urls import path
from dashboard.views import history as history

urlpatterns = [
    path('history/', history.history_view, name='history'),
]
