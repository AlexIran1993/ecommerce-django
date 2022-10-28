from django.db import models
#Instaciamiento de la clase Category
from category.models import Category
from django.urls import reverse
from accounts.models import Account
#Libreria usada para obtener un promedio
from django.db.models import Avg, Count
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
    images = models.ImageField(upload_to = 'photos/products', blank = True)
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

    #Metodo para cualcular el promedio de los ratings
    def averageReview(self):
        #Obtencion del producto filtrando por la data del producto y el estado.
        #Ejecucion de la funcion que obtenga el promedio con respecto a la columna rating
        reviews = ReviewRating.objects.filter(product=self, status = True).aggregate(average = Avg('rating'))

        avg = 0
        #Si en la propiedad average del objeto reviews no es nulo, asigno el valor a la propiedad avg.
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    #Metodo que contara las cantidad de comentarios hehchos
    def countReview(self):
        reviews = ReviewRating.objects.filter(product = self, status = True).aggregate(count =Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

#Clase que filtrara los variation de los productos
class VariationManager(models.Manager):
    #Metodo para solo retornar los variantions de color
    def colors(self):
        #Retorno los variations con el filtro de color y que sean activos
        return super(VariationManager, self).filter(variation_category ='color', is_active=True)
        #Metodo para solo retornar los variantions de talla
    def tallas(self):
        #Retorno los variations con el filtro de talla y que sean activos
        return super(VariationManager, self).filter(variation_category ='talla', is_active=True)

#Valores preexistentes del choise
variation_category_choice = (
    ('color', 'color'),
    ('talla', 'talla'),
)

#Entidad para los variants de los prductos.
class Variation(models.Model):
    #Llave foranea para la clase Product
    product = models.ForeignKey(
        #Clase que sera isntanciada
        Product,
        #dependencia que cuando se elimine el producto tambien se eliminara el variation automaticamnete
        on_delete=models.CASCADE
    )
    #Nombre del variation 
    variation_category = models.CharField(
        max_length=100,
        #Elementos seleccionables ya preexistentes
        choices=variation_category_choice
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    #Instancia de VariationManager
    objects = VariationManager()

    def __str__(self):
        return self.variation_category + ':' + self.variation_value

#Entidad para la seccion de comentarios y puntajes
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    #Campós visibles en el Grid de ReviewRating
    def __str__(self):
        return self.subject

#Modelo para la colleccion de imaganes de los productos en el template product_details.html
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'store/products', max_length = 225)

    def __str__(self):
        return self.product.product_name
