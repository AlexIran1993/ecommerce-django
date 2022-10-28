from django.contrib import admin
from .models import Category
# Register your models here.

#Clase usada para el manejo de slugs den las categorias
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        #Indico cual propiedad se va autollenar / Se llenara con los valores de category_name
        'slug': ('category_name',)
    }
    #Elemetos que se mostraran el el grid de la lista de categorias
    list_display = ('id','category_name', 'slug')

#paso como parametro la clase CategoryAdmin
admin.site.register(Category, CategoryAdmin)
