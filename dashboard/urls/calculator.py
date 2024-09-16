from django.urls import path
from dashboard.views import calculator as calculator

urlpatterns = [
    path('calculator/', calculator.CalculatorView.as_view(), name='calculator'),
    path('calculator_result/', calculator.CalculatorResultView.as_view(), name='calculator_result'),
]
