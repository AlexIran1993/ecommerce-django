from django.urls import path
from . import views


#Lista de paths que ejecutaran los metodos de views.py
urlpatterns = [
    path('', views.store, name="store"),

    #Path usado para el llamado de una categoria
    path(
        #Asigno el valor de la propiedad category_slug a una variable llamada slug
        'category/<slug:category_slug>/',
        #ejecucion del metodo def que se ejecutara en el models.py
        views.store,
        #Nombre del path
        name="products_by_category"
    ),

    #Path con el slug de la categoria y el producto
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    #Path para el campo de busqueda 
    path('search', views.search, name='search'),
    #Path que procesara el formulario comenatrio
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]