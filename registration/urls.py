from django.urls import path
from .views import *

urlpatterns = [
    path('submit/<str:etype>/<int:pid>/', submit_reg, name='submit-reg'),
    path('complete/<str:etype>/<int:pid>/', complete_reg, name='complete-reg'),
]