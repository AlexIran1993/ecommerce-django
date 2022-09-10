from django.db import models
from accounts.models import Account
from store.models import Product, Variation
# Create your models here.

#Clase para la entidad Payment
class Payment(models.Model):
    #Objeto llave foranea que representa a la clase Account
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    pyament_id = models.CharField(max_length=100)
    pyament_method = models.CharField(max_length=100)
    amount_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #Propiedad que se mostraran en el grid de Django
        return self.pyament_id

#Clase para la entidad Order
class Order(models.Model):

    #Diccionario con los status disponibles
    STATUS = (
        #Layer / Valor
        ('New', 'Nuevo'),
        ('Accepted', 'Aceptado'),
        ('Completed', 'Completado'),
        ('Cancelled', 'Cancelado'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    emails = models.CharField(max_length=50)
    addres_line_1 = models.CharField(max_length=100)
    addres_line_2 = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    #Funcion que me concatene el nombre y apellido del usuario
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    #Concatenacion de las direcciones
    def full_addres(self):
        return f'{self.addres_line_1} {self.addres_line_2}'

    def __str__(self):
        return self.first_name

#Clase para la entidad Order Products
class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name