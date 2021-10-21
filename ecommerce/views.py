from django.shortcuts import render

from store.models import Product

def home(request):
    #LIsta de productos que sera retornada al home.html / Solo traere a los productos que esten activos en BD
    products = Product.objects.all().filter(is_availible = True)

    #Alamceno la lista en in Json
    context = {
        'products': products
    }

    #Envio el Json como parametro junto con el request del cliente y la ejecucion del template
    return render(request, 'home.html', context)