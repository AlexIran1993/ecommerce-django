from django.db import models
from django.urls import reverse
# Create your models here.

#Entidad de las categorias de la web application.
class Category(models.Model):
    #Propiedad que representa al nombre de la categoria/ sera de valor unico.
    category_name = models.CharField(max_length=20, unique=True)
    #Propiedad para la descripcion que permitira valores unicos.
    description = models.CharField(max_length=225, blank=True)
    #Esta propiedad sera usada para representar a la entidad en la parte final de la url.
    slug = models.CharField(max_length=100, unique=True)
    #Esta propiedad sera usada para colocar una imagen en la categoria/ se indica la direccion de la imagen y que puede ser nula. 
    cat_image = models.ImageField(upload_to = 'photos/categories', blank = True)

    #Indicacion del nombre reflejado en django administration.
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    #Esta data sera visible en el dashboar de Django
    def __str__(self):
        return self.category_name
    
    #Metodo que extrae el link con la categoria
    def get_url(self):
        return reverse(
            #Nombre del path que contiene la url con el valor de slug de la categoria
            'products_by_category',
            #Argumento agregado que sera el valor de slug
            args = [self.slug]
        )
