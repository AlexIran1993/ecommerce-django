from django.urls import path
from . import views

urlpatterns = [
    path('new_category/', views.new_category, name="nueva_categoria"),
]