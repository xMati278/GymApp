from django.urls import path
from .views import GetAllBodyParts, Calculate1RM, CalculateWilks, CalculateDots, CalculateIpfGl, CalculateTotal

urlpatterns = [
    path('1rm/', Calculate1RM.as_view(), name='calculate-1rm'),
    path('wilks/', CalculateWilks.as_view(), name='calculate-wilks'),
    path('dots/', CalculateDots.as_view(), name='calculate-dots'),
    path('ipfgl/', CalculateIpfGl.as_view(), name='calculate-ipf-gl'),
    path('total/', CalculateTotal.as_view(), name='calculate-total'),
    path('bodyparts/', GetAllBodyParts.as_view(), name='get-all-body-parts'),
]
