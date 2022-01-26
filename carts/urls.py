from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    #Path para el template home dentro de carts/
    path('', views.cart, name='cart'),
    path(

        #Url que se ejecutara al seleccionar el producto.
        #Envio como parametro el id del producto.
        'add_cart/<int:product_id>/', 
        #Metodo def dentro de views.py que se ejecutara al enviar el http://localhost:8000/carts/
        views.add_cart,
        #Nombre del path 
        name='add_cart'
    ),
    #Path para invocar el remove
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    #Path para la eliminacion de un producto en la tabla CartItem
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name = 'remove_cart_item'),
    #Path para drijir al usuario al template de checkout
    path('checkout/', views.checkout, name='checkout'),
]