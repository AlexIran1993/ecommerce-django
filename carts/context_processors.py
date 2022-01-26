#Importacion de las clases Cart y CartItem
from .models import Cart, CartItem
#Importacion que me permite buscar el carrito de compras del usuairo en session
from  .views import _cart_id

#Funcion global
def counter(request):
    #Variable que almacenara la cantidad de productos en el carrito de compras, por defecto sera 0
    cart_count = 0

    try:
        #Busco el carrito de compras con la funcion _cart_id que importe desde cart.views.
        cart = Cart.objects.filter(cart_id = _cart_id(request))

        #Condicion para saber si el usuario esta en sesion
        if request.user.is_authenticated:
            #Hago una busqueda de los productos del carrito de compras usando como filtro la data del usuario
            cart_items = CartItem.objects.all().filter(user = request.user)
        else:
            #Busco los elementos del carrito de compras
            cart_items = CartItem.objects.all().filter(cart = cart[:1])

        #Extraigo el total de los valores de quantity de cada uno de los itmes de cart_items
        for cart_item in cart_items:
            #Almaceno el valor de cada propiedad quantity en la variable cart_count
            cart_count += cart_item.quantity
    #En caso de que no exista carrito retorno el cart_count con cero
    except Cart.DoesNotExist:
        cart_count = 0
    #Retorno la varibale cart_count con la cantidad de prodcutos del carrito en un Json
    return dict(cart_count = cart_count)