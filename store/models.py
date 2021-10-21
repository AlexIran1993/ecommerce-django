from django.db import models
#Instaciamiento de la clase Category
from category.models import Category
from django.urls import reverse
# Create your models here.

#Clase que representa a la entidad del producto
class Product(models.Model):
    # Nombre del produto/ Valor unico
    product_name = models.CharField(max_length=200, unique=True)
    #Slug del url
    slug = models.CharField(max_length=200, unique=True)
    #Descripcion del producto / Valor unico
    decription = models.TextField(max_length=500, blank=True)
    #Precio del producto
    price = models.IntegerField()
    #Imagen del producto / Direccion donde se alamacenara la imagen
    images  =models.ImageField(upload_to = 'photos/products')
    #Verificacion de productos en stock
    stock = models.IntegerField()
    #Verificacion de si el producto esta en existencia
    is_availible = models.BooleanField(default=True)
    #Llave foranea de la entidad Category
    category = models.ForeignKey(
        #Instanciamiento de la clase Category 
        Category, 
        #Cuando se elimina una categoria, se eliminaran los productos ligados a esta categoria
        on_delete=models.CASCADE
    )
    #Fecha de creacion / Se asignara de manara automatica la fecha de ese dia
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    #Metodo que generara una url dimanica segun el producto
    def get_url(self):
        #Retorno de la url base con la agregacion del path product_details
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
