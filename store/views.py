import re
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, ProductGallery, ReviewRating
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
#Libreria usada para la paginacion de productos
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#Libreria usada para la consulta
from django.db.models import Q
from .forms import ReviewForm, ProductForm
from django.contrib import messages
from orders.models import OrderProducts
from django.contrib.auth.decorators import login_required
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
        products = Product.objects.filter(category = categories, is_availible = True).order_by('id')

        #Instancia de Paginator
        paginator = Paginator(
            #Parametro que determinara los productos extraidos de la base de datos
            products,
            #Valor que representa la cantida de elemtos que integrara cada pagina
            5
        )
        
        #Extraigo el id de la pagina a la que quiero acceder.
        page = request.GET.get('page')

        #Lista de productos de la pagina 'page'
        paged_products = paginator.get_page(page)

        #Cantidad de productos 
        products_count = products.count()
        #Cantidad de productos peretenecientes a la categoria
        products_count = products.count()

    #De otra manera traigo todos los productos existentes
    else:
        #Lista de productos extraida de la base de datos / solamente los que tengan la casilla de activos
        products = Product.objects.all().filter(is_availible = True).order_by('id')

        #Instancia de Paginator
        paginator = Paginator(
            #Parametro que determinara los productos extraidos de la base de datos
            products,
            #Valor que representa la cantida de elemtos que integrara cada pagina
            5
        )
        #Extraigo el id de la pagina a la que quiero acceder.
        page = request.GET.get('page')

        #Lista de productos de la pagina 'page'
        paged_products = paginator.get_page(page)
        
        #Cantidad de productos 
        products_count = products.count()

    #Objeto Json que contendra la lista de los productos extraidos en BD
    context = {
        'products':paged_products,
        'products_count': products_count,
    }

    #Envio como parametro el objeto Json.
    return render(request, 'store/store.html', context )


@login_required(login_url="login")
def nuevo_producto(request):
    if request.user.is_admin == False:
        messages.warning(request, 'NO TIENES ACCESO A ESTE NIVEL')
        return render(request, 'accounts/dashboard.html')
        
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            decription = form.cleaned_data['decription']
            price = form.changed_data['price']
            images = form.cleaned_data['images']
            stock = form.changed_data['stock']
            category = form.cleaned_data['category']

            sin_caracters = re.sub(r"[^\w\s]", '', product_name)
            slug = re.sub(r"\s+", "-", sin_caracters)

            producto = Product.objects.create(
                product_name = product_name,
                decription = decription,
                price = price,
                images = images,
                stock = stock,
                category = category,
                slug = slug.lower()
            )
            producto.save()
            messages.success(request, 'El producto ' + product_name + ' se ha creado exitosamente.')
        else:
             messages.error(request, 'El producto se ha creado exitosamente.')

    context ={
        'form': form
    }
    return render(request,'store/new_product.html', context)

#Metodo def para el template del detallado del producto
#Parametros que llegan: request del cliente, valor slug de la categoria y valor slug del producto
def product_detail(request, category_slug, product_slug):

    #Verifico que el slug del producto exista
    try:
        #Traigo el producto de la base de datos.
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        #Verificare si un producto ya esta en el carrito de compras
        in_cart = CartItem.objects.filter(
            #Obtengo el id de la pripieda cart_id la cual aceedo a travez del objeto/propiedad cart.
            # Lo comparo con el cart del usuario en session.
            cart__cart_id = _cart_id(request),
            #Comparo el valor del priduct con el single_product
            product = single_product
        #Si al ejecutar existe un record en in_cart el metodo .exist() retornara un true.
        ).exists()
    except Exception as e:
        #En caso de que el producto no exista en base de datos se disparara esta excepcion.
        raise e

    #Si el usuario esta logiado, intento traer el historial de compras de esete usuario
    if request.user.is_authenticated:
        #Triago el historial de compras de este cliente
        try:
         orderproduct = OrderProducts.objects.filter(user = request.user, product_id = single_product.id).exists()
        except OrderProducts.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    #Traigo los comentarios hehcos a este producto
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status = True)

    #Query que obtendra la lista de imagenes ligada al producto
    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)
    

    #Añado el resultado en un objeto Json
    context = {
        'single_product': single_product,
        'in_cart':in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        #Collection de imagenes ligado al producto
        'product_gallery': product_gallery
    }

    #Retorno del request al template product_details.html / Envio el Json Como parametro.
    return render(request, 'store/product_details.html', context)

#Def para la busqueda de productos
def search(request):
    #Valido que se reciva el parametro keyword y en caso de que asi sea lo almaceno en una variable
    if 'keyword' in request.GET:
        #Alamacenaminto de keyword
        keyword=request.GET['keyword']
        #Si el kword es real traere la lista de productos que se relacionen con el keyword
        if keyword:
            #Lista de productos relacionados al keyword de manera desendente.
            products=Product.objects.order_by('-created_date').filter(
                #Condicion que tendra el query para la lista de productos
                #Para recorrer todas las palabras de la descripcion o del nombre como una lista
                #usare la propiedad icontains accediendo a ella con un doble guion bajo.
                Q(decription__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            #Contador de productso
            products_count=products.count()
            #Json con la lista y contador de los productso
    products=None
    products_count=0
    context = {
        'products':products,
        'products_count': products_count,
    }

    #Llamado y enviado del json al template 
    return render(request, 'store/store.html', context)

#Metodo def que procesara el formulario Comentario
def submit_review(request, product_id):
    #Captura del la url
    url = request.META.get('HTTP_REFERER')
    #Validar que exista un POST en el request
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Muchas gracias!, tu comentario ha sido actualiizado')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Muchas gracias, tu comentario fue enviado con exito!')
                return redirect(url)