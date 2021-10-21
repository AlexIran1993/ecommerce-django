from django.urls import path
from . import views


#Lista de paths que ejecutaran los metodos de views.py
urlpatterns = [
    path('', views.store, name="store"),

    #Path usado para el llamado de una categoria
    path(
        #Asigno el valor de la propiedad category_slug a una variable llamada slug
        '<slug:category_slug>/',
        #ejecucion del metodo def que se ejecutara en el models.py
        views.store,
        #Nombre del path
        name="products_by_category"
    ),

    #Path con el slug de la categoria y el producto
    path(
        #Slug de la categoria y prodcuto
        '<slug:category_slug>/<slug:product_slug>/',
        #Ejecucion del metodo def dentro de models.py
        views.product_detail,
        #Nombre del path
        name='product_detail'
    ),
]