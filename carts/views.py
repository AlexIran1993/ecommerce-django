from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
#Libreria que me condiciona el acceso a los componentes del proyeco
from django.contrib.auth.decorators import login_required
# Create your views here.

#Funcion que treara la sesion actual del browser
def _cart_id(request):
    #Extraccion de la llave de sesion del usuario
    cart = request.session.session_key
    #Condicion en caso de que el cart no exista
    if not cart:
        cart = request.session.create()
    return cart

#Funcion para crear el carrito de compra con los productos seleccionados
def add_cart(request, product_id):
    #Busqueda del producto seleccionado a travez con product_id
    product = Product.objects.get(id = product_id)

    #Obtengo el usuario que este en sesion
    current_user = request.user
    #Valido si la variable tiene un usuario en sesion
    if current_user.is_authenticated:
        #Logica para añadir productos al carrito de compras cuando el usuario esta en sesion
        #Variable collection que almacenara las variations
        product_variation = []

        #Evaluacion del metodo de envio sea un POST
        if request.method == 'POST':
            #Bucle para capturar los variations que contenga el body del request
            for item in request.POST:
                #Captura del nombre del variation
                key = item
                #Captura del valor del variation
                value = request.POST[key]
            
                #Validacion que el variation se encuentre en la base de datos
                try:
                    variation = Variation.objects.get(
                        #Producto al que se aplicara la busqueda del variations
                        product=product, 
                        #Variation que se buscara 
                        variation_category__iexact=key,
                        variation_value__iexact=value
                        )
                    #Añadicion del variation a la collecion
                    product_variation.append(variation)
                except:
                    pass
            
        #Variable para saber si el cart_item seleccionado existe usando como filtro el product y user
        is_cart_item_exist = CartItem.objects.filter(product = product, user = current_user).exists()

        #Inserccion del item al carrito de compra
        if is_cart_item_exist:
            #Variable que almacenara al producto extraido de base de datos y es almacenado en product.
            #Le asigno el valor de cart que representa el carrito de compra del usuario en session.
            cart_item = CartItem.objects.filter(product = product, user = current_user)

            #Captura de los variations del registro de la base de datos
            ex_var_list = []
            #Captura de los id de todos los variatiosn
            id = []
            #Recorrido de la lista de variations del objeto cart_item:
            for item in cart_item:
                #Almaceno los variation en una variable
                existing_variations = item.variations.all()
                #Agrego a la lista los variations extraidos del obejto cart_item/ convierto la variable a una lista 
                ex_var_list.append(list(existing_variations))
                #Agrgeo el id de cada variation a la lista id
                id.append(item.id)

            #Validacion de los variations del registro con el producto seleccioando por el usuario
            if product_variation in ex_var_list:
                #Actualizo la cantidad de productos del registro que existe en base de datos
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()
            #En caso de que los variations no coincidan creo un nuevo regstro con el producto seleccioando
            else:
                item = CartItem.objects.create(product = product, quantity  = 1, user = current_user)
                #Logica para la inserccin del variation al cart_item, solo el caso de que la collection no este en blanco
                if len(product_variation) > 0:
                    #Limpieza de los variatins ya existentes
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()
        
        else:
            cart_item = CartItem.objects.create(product = product, quantity = 1, user = current_user,)

            #Logica para la inserccin del variation al cart_item, solo el caso de que la collection no este en blanco
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')
    else:
        #Variable collection que almacenara las variations
        product_variation = []

        #Evaluacion del metodo de envio sea un POST
        if request.method == 'POST':
            #Bucle para capturar los variations que contenga el body del request
            for item in request.POST:
                #Captura del nombre del variation
                key = item
                #Captura del valor del variation
                value = request.POST[key]
            
                #Validacion que el variation se encuentre en la base de datos
                try:
                    variation = Variation.objects.get(
                        #Producto al que se aplicara la busqueda del variations
                        product=product, 
                        #Variation que se buscara 
                        variation_category__iexact=key,
                        variation_value__iexact=value
                        )
                    #Añadicion del variation a la collecion
                    product_variation.append(variation)
                except:
                    pass
            
        #Creaccion del carrito de compras
        try:
            #Ejecuto la funcion _cart_id que me traera el carrito del usuario en session
            cart = Cart.objects.get(cart_id = _cart_id(request))

        except Cart.DoesNotExist:
            #En caso de que no existe un carrito de compras en base de datos  lo creo.
            cart = Cart.objects.create(cart_id = _cart_id(request))
            #Guardado del registro 
            cart.save()

        #Variable para saber si el cart_item seleccionado existe
        is_cart_item_exist = CartItem.objects.filter(product = product, cart=cart).exists()

        #Inserccion del item al carrito de compra
        if is_cart_item_exist:
            #Variable que almacenara al producto extraido de base de datos y es almacenado en product.
            #Le asigno el valor de cart que representa el carrito de compra del usuario en session.
            cart_item = CartItem.objects.filter(product = product, cart = cart)

            #Captura de los variations del registro de la base de datos
            ex_var_list = []
            #Captura de los id de todos los variatiosn
            id = []
            #Recorrido de la lista de variations del objeto cart_item:
            for item in cart_item:
                #Almaceno los variation en una variable
                existing_variations = item.variations.all()
                #Agrego a la lista los variations extraidos del obejto cart_item/ convierto la variable a una lista 
                ex_var_list.append(list(existing_variations))
                #Agrgeo el id de cada variation a la lista id
                id.append(item.id)

            #Validacion de los variations del registro con el producto seleccioando por el usuario
            if product_variation in ex_var_list:
                #Actualizo la cantidad de productos del registro que existe en base de datos
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id = item_id)
                item.quantity += 1
                item.save()
            #En caso de que los variations no coincidan creo un nuevo regstro con el producto seleccioando
            else:
                item = CartItem.objects.create(product = product, quantity  = 1, cart = cart)
                #Logica para la inserccin del variation al cart_item, solo el caso de que la collection no este en blanco
                if len(product_variation) > 0:
                    #Limpieza de los variatins ya existentes
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()
        
        else:
            cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart,)

            #Logica para la inserccin del variation al cart_item, solo el caso de que la collection no este en blanco
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

#Funcion usada para remover items de carrito de compras
def remove_cart(request, product_id, cart_item_id):
    #Busqueda del prodcuto en la base de datos 
    product = get_object_or_404(
        #Tabla donde se encuentra el prodcuto.
        Product,
        #Id del producto a buscar en Product.
         id = product_id
    )
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        #Evaluacion del los elementod del carrito
        if cart_item.quantity>1:
            #Elimino un elemento de la propiedad quantity del objeto cart_item
            cart_item.quantity -=1
            #Guardo los cambios en base de datos
            cart_item.save()
        else:
            #En caso de que la proiedad quantity de cart_item sea menor a 1, eliminare por completo el producto
            cart_item.delete()
    except:
        pass

    #Redirecciono al metodo cart
    return redirect('cart')

#Elimianar un producto del carrito de compra
def remove_cart_item(request, product_id, cart_item_id):
    #Traere el producto de la base de datos    
    product = get_object_or_404(Product, id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        #Instancio la clase CartItem con el producto a eliminar
        cart_item = CartItem.objects.get(product = product, cart=cart, id=cart_item_id)

    #Elimino el registro de la tabla CartItem
    cart_item.delete()
    #Redirecciono al metodo cart
    return redirect('cart')

#Funcion para el home en carts
#En esta funcion se llevara a cabo la logica para traer el producto que el usuario comprara
def cart(request, total = 0, quantity =  0, cart_items = None):
    tax = 0
    grand_total = 0
    #Consulta a base de datos
    try:

        #Condicion para saber si el usuario esta en sesion
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            #Traigo el cart del usuario 
            cart = Cart.objects.get(cart_id = _cart_id(request))
            #cart_item que pertenecen al cart del usuario
            cart_items = CartItem.objects.filter(cart = cart, is_active = True)

        #Bucle que sumara el precion total de los productos seleccionados
        for cart_item in cart_items:
            #Precio total 
            total += (cart_item.product.price * cart_item.quantity)
            #Cantidad total de productos
            quantity += cart_item.quantity
        
        #Calculo del impuesto que sera el 2%
        tax = (2*total)/100
        #Total final
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    #Objeto Json que coontendra el carrito de compras con los items seleccionado
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'store/carts.html', context)

@login_required(login_url='login')
def checkout(request, total = 0, quantity =  0, cart_items = None):
    tax = 0
    grand_total = 0
    #Consulta a base de datos
    try:
        #Condicion para saber si el usuario esta en sesion
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            #Traigo el cart del usuario 
            cart = Cart.objects.get(cart_id = _cart_id(request))
            #cart_item que pertenecen al cart del usuario
            cart_items = CartItem.objects.filter(cart = cart, is_active = True)

        #Bucle que sumara el precion total de los productos seleccionados
        for cart_item in cart_items:
            #Precio total 
            total += (cart_item.product.price * cart_item.quantity)
            #Cantidad total de productos
            quantity += cart_item.quantity
        
        #Calculo del impuesto que sera el 2%
        tax = (2*total)/100
        #Total final
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    #Objeto Json que coontendra el carrito de compras con los items seleccionado
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'store/checkout.html', context)

