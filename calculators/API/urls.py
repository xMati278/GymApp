from django.urls import path
from calculators.API import views

urlpatterns = [
    path('1rm/', views.Calculate1RM.as_view(), name='calculate-1rm'),
    path('wilks/', views.CalculateWilks.as_view(), name='calculate-wilks'),
    path('dots/', views.CalculateDots.as_view(), name='calculate-dots'),
    path('ipfgl/', views.CalculateIpfGl.as_view(), name='calculate-ipf-gl'),
    path('total/', views.CalculateTotal.as_view(), name='calculate-total'),
]
