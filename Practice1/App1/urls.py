
from django.contrib import admin
from django.urls import path,include
from . import views 

urlpatterns = [
   
    path('',views.addStudent),
    path('addSubject/',views.addSubject),
    path('getstudent/',views.getstudent),
]
