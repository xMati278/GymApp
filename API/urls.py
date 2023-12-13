from django.urls import path
from .views import calculate_total, calculate_1rm, calculate_wilks, calculate_dots, calculate_ipf_gl

urlpatterns = [
    path('1rm/', calculate_1rm, name='calculate-1rm'),
    path('wilks/', calculate_wilks, name='calculate-wilks'),
    path('dots/', calculate_dots, name='calculate-dots'),
    path('ipfgl/', calculate_ipf_gl, name='calculate-ipf-gl'),
    path('total/', calculate_total, name='calculate-total'),
]