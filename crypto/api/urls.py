from django.urls import path
from .views import OverallAV, CryptoDetailAV, ConvertAV

urlpatterns = [
    path('overall/', OverallAV.as_view(), name='overall'),
    path('overall/<slug:slug>/',CryptoDetailAV.as_view(), name='crypto-detail'),
    path('convert/', ConvertAV.as_view(), name='convert')
]