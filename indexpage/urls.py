from django.urls import path
from . import views

app_name= "indexpage"
urlpatterns = [
    path('', views.index, name='index')
]