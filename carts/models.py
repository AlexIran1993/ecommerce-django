from django.db import models
from django.db.models.deletion import CASCADE
#Clase que representa a los productos en base de datos
from store.models import Product, Variation
from accounts.models import Account
# Create your models here.

#Clase para el carrito de compras
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now=True)

    #Metodo def usado para selccionar una propieda que se pintara en la tabla
    def __str__(self):
        return self.cart_id


#Clase para el prodcuto que se añadira al carrito
class CartItem(models.Model):
    #Propiedad que se relacione con el usuario en sesion
    user = models.ForeignKey(Account, on_delete=CASCADE, null=True)
    #Propiedad que represenatara al producto seleccionado para la compra
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #Propiedad que representa al carrito de compras del usuario en session.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    #Cantidad de elemtos del producto seleccioando
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    #Propiedad que almacenara la coleccion de variations del producto agregado a Cart
    variations = models.ManyToManyField(
        #Almacenamiento de un conjuto de Varitaions
        Variation, blank=True
    )

    #Def que calcula el subtotal de cada producto
    def sub_total(self):
        return(self.product.price * self.quantity)

    #Modificare esta funcion para solucionar el problema de asignacion de productos al carrito de compras
    #Cambiare el def __str__ a def __unicode__
    def __unicode__(self):
        return self.product