from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category

# Create your views here.

#metodo def que recive el request del cliente y una propiedad que representa al slug que por el momento es nulo.
def store(request, category_slug=None):
    #Condicion para saber si se esta aplicando un filtro
    categories = None
    products = None

    #En caso de de que la varible category_slug sea diferente a nulo, aplicare un filtro 
    if category_slug != None:
        #Alamceno en una lista las categorias que coincidan con el valor de category_slug
        categories = get_object_or_404(Category, slug=category_slug)
        #Aplico el filtro que obtuve en categories para traer los productos asociados a el 
        products = Product.objects.filter(category = categories, is_availible = True)
        #Cantidad de productos peretenecientes a la categoria
        products_count = products.count()

    #De otra manera traigo todos los productos existentes
    else:
        #Lista de productos extraida de la base de datos / solamente los que tengan la casilla de activos
        products = Product.objects.all().filter(is_availible = True)
        #Cantidad de productos 
        products_count = products.count()

    #Objeto Json que contendra la lista de los productos extraidos en BD
    context = {
        'products': products,
        'products_count': products_count
    }

    #Envio como parametro el objeto Json.
    return render(request, 'store/store.html', context )

#Metodo def para el template del detallado del producto
#Parametros que llegan: request del cliente, valor slug de la categoria y valor slug del producto
def product_detail(request, category_slug, product_slug):

    #Verifico que el slug del producto exista
    try:
        #Traigo el producto de la base de datos.
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        #En caso de que el producto no exista en base de datos se disparara esta excepcion.
        raise e

    #Añado el resultado en un objeto Json
    context = {
        'single_product': single_product
    }

    #Retorno del request al template product_details.html / Envio el Json Como parametro.
    return render(request, 'store/product_details.html', context)
