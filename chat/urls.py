from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name='index'),
    path('<str:first>/<str:last>/' , views.room , name='room')

]