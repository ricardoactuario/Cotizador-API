from django.urls import path
from . import views

urlpatterns = [
    path('SeguroAccidentesPersonalesIndividual/', views.CotizadorAP)
]