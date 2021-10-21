from django.contrib import admin
from .models import Product
# Register your models here.

#Propiedades que se enlistaran el el grid de django
class ProductAdmin(admin.ModelAdmin):
    #Lista de propiedades que se mostraran en el gris
    list_display = (
        'product_name',
        'price',
        'stock',
        'category',
        'modified_date',
        'is_availible'
    )
    #Prellenedado de ciertos campos
    prepopulated_fields = {
        #El campo slug se llenara con la data de 'product_name'
        'slug' : ('product_name',)
    }

#Registro de la entidad de Product
admin.site.register(Product, ProductAdmin)
