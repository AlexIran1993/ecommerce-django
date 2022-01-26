from django.contrib import admin
from .models import Product, ReviewRating, Variation
# Register your models here.

#Propiedades que se enlistaran el el grid de django
class ProductAdmin(admin.ModelAdmin):
    #Lista de propiedades que se mostraran en el grid
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

#Clase que contendra una lista con las propiedades que se mostraran en el grid del model Variations
class VariationsAdmin(admin.ModelAdmin):
    #Liasta con las propiedades
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'is_active'
    )
    #Propiedades que pueden ser modificadas desde el grid.
    list_editable = ('is_active',)
    #Filtros que deseo activar
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')

#Registro de la entidad de Product
admin.site.register(Product, ProductAdmin)
#Registro de la entidad Variant para los variants de cada producto
admin.site.register(Variation, VariationsAdmin)
#Registro de la entidad ReviewRating
admin.site.register(ReviewRating)