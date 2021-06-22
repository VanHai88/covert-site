from django.urls import path

from .views import (
    att_list,
    user_att_detail,
)

urlpatterns = [
    path('all/', att_list, name='attendances-list'),
    path('user/<str:username>/',
         user_att_detail, name='user-att-detail'),
]
