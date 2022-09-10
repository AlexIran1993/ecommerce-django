from django.urls import path
from  . import views

#Arreglo de paths para las funciones dentro de views.
urlpatterns = [
    #Path de la funcion place_order
    path('place_order/', views.place_order, name='place_order'),
    #Path de la funcion payment
    path('payments/', views.payments, name='payments'),
    #Path de la funcion order_complete
    path('order_complete/', views.order_complete, name='order_complete'),
]