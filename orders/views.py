from django.http import JsonResponse
from django.shortcuts import redirect, render
from carts.models import CartItem
from .models import Order, OrderProducts, Payment
from .forms import OrderForm
from store.models import Product
import datetime
import json
#Librerias necesarias para enviar un correo electronico
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

def place_order(request, total = 0, quantity = 0):
    #Captura de los datos del usuario en sesion
    current_user = request.user
    #Captura de los itmes dentro del carrito de compras
    cart_items = CartItem.objects.filter(user = current_user)
    #Contador de elementod que contenga el carrito de compras
    cart_count = cart_items.count()

    #Si el contador es 0, redijire al usuario a store
    if cart_count <= 0:
        return redirect('store')

    #Variables usadas para calcular el impuesto y total a pagar
    grand_total = 0
    tax = 0

    for car_item in cart_items:
        #Costo de todos los elementos del mismo producto
        total += (car_item.product.price * car_item.quantity)
        #Cantidad de elementod del mismo producto
        quantity = car_item.quantity

    #Impuesto  del 2% a pagar
    tax = (2 * total)/100
    #Total a pagar con impuestos agrgados
    grand_total = total + tax

    if request.method == 'POST':
        #Instanciamiento de OrderForm()
        form = OrderForm(request.POST)

        if form.is_valid():
            #Instaciamiento de la clase Order
            data = Order()
            #Construyo el objeto data con la informacion del formulario
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.emails = form.cleaned_data['emails']
            data.addres_line_1 = form.cleaned_data['addres_line_1']
            data.addres_line_2 = form.cleaned_data['addres_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            #Obtencion de la ip del usuario
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #Creacion de la fecha de hoy por año/mes/dia
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            #Fecha de hoy 
            d = datetime.date(yr,mt,dt)
            #Numero de orden creada con la fecha de hoy (sin las digianoles)
            current_date = d.strftime("%Y%m%d")

            #Numero de orden concatenedo con el id de la orden
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            #Extaccion del registro de la tabla order.
            order = Order.objects.get(
                #Parametro por el que buscare el registro en la tabla Order
                user = current_user, 
                #Indicacion de que la orden este en status de ordenada
                is_ordered = False,
                #Parametro de nuemero de orden generado anteriormente
                order_number = order_number

            )

            #Objeto Json con la data que sera enviada a el template payment.html
            context = {
                #Objeto con la orden
                'order':order,
                #Carrito con los productos a comprar
                'cart_items':cart_items,
                #Total a pagar sin inpuestos
                'total':total,
                #Impuesto calculado
                'tax':tax,
                #Total a pagar con impuestp
                'grand_total':grand_total,
            }

            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')

def payments(request):

    #Variable que almacenara el Json dentro del body del request
    body = json.loads(request.body)
    #Busco la orden de comopra usando como parametros el user, que la ordern no haya sido completada y el valor de la propiedad orderID del body.
    order = Order.objects.get(user = request.user,  is_ordered = False, order_number = body['orderID'])
    #Creacion del objeto Pyament usando como parametro los vlores del objeto order
    payment = Payment(
        user = request.user,
        pyament_id = body['transID'],
        pyament_method = body['payment_method'],
        amount_id = order.order_total,
        #Valor obtenido por Paypal
        status = body['status'],
    )

    payment.save()

    #Almaceno la data del objeto payment en el foreykey payment de la tabla Order
    order.payment = payment
    #Cambio la orden como True en señal de que la orden fue completada
    order.is_ordered = True
    email = order.emails 
    order.save()

    #registro dentro de la tabla OrderProduct de los productos en el CartItem
    #Busqueda de los productos seleccionados por el usuario en sesion
    cart_items = CartItem.objects.filter(user=request.user)

    #Recorrdio de la lista de productos 
    for item in cart_items:
        #Instanciamiento de la clase OrderProduct()
        orderproduct = OrderProducts()
        #Llenado de la data perteneciente a la orden de compra y almacenado en base de datos
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        #Almacenamiento de los variations de cada producto
        cart_items = CartItem.objects.get(id = item.id)
        product_variation = cart_items.variations.all()
        orderproduct = OrderProducts.objects.get(id= orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
    
        #Decrecimiento del stock del productos segun la cantidad comprada por el usuario
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    #Eliminacion del carrito de compras
    CartItem.objects.filter(user = request.user).delete()

    #Envio del correo elctronico de confirmacion de compra
    #Titulo del mensaje
    mail_subject = 'Gracias por tu compra'
    #Template con el curepo del mail mas los parametros a enviar
    body = render_to_string('orders/order_recieved_email.html',{
        'user': request.user,   
        'order': order,
    })

    #Creacion del correo con los components creados
    send_email = EmailMessage(mail_subject, body, to=[email])
    #Envio del correo electronicos
    send_email.send()

    #Objeto Json con la data que enviare al template order_number
    data = {
        'order_number': order.order_number,
        'transID': payment.pyament_id,
    }

    return JsonResponse(data)


def order_complete(request):
    #Captura del orden_number
    order_number = request.GET.get('order_number')
    #Captura del transID
    transID = request.GET.get('payment_id')

    try:
        #Busqueda de la orden
        order = Order.objects.get(order_number = order_number, is_ordered=True)
        #Busqueda de los productos de la compra de manera ordenada
        ordered_products = OrderProducts.objects.filter(order_id = order.id)

        #Calculo del subtotal de la compra
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        
        #Captura del payment
        payment = Payment.objects.get(pyament_id = transID)

        #Data que enviare al template
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.pyament_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')