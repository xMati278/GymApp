from django.urls import path
from dashboard.views import record as record

urlpatterns = [
    path('records/', record.records_view, name='records'),
]
