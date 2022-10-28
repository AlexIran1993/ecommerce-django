from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from orders.models import Order
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
# Funciones necesarias para ligar el carrito de compras a la sesion del usuario
from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

# Create your views here.
# Metodo def para el regsitro de un nuevo usuaruio

# Metodo def para la ejecucion de la logica correspondiente al regsitro de nuevos usuarios.
def register(request):
    # Instancia de la clase que contiene el modelo para el registro de usuarios
    form = RegistrationForm()
    # Valido que el request llegue con un metodo post en el body
    if request.method == 'POST':
        # Instaciamiento de Regitrationform
        form = RegistrationForm(request.POST)
        # Si el objeto es valido, capturare los datos que esta enviando el cliente
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_numer = form.cleaned_data['phone_numer']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Creacion del usernamer usando el email.
            username = email.split("@")[0]

            # Creacion del usuario en base de datos
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_numer = phone_numer
            # Almacenamieto del usuario en base de datos
            user.save()

            #Creacion de un nuevo registro en la tabla UserProfile ligado a este nuevo usuario
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'defualt/defualt-user.png'
            profile.save()

            # Proceso de activacion del usuario
            current_site = get_current_site(request)
            # Titulo del correo electronico
            mail_subject = 'Activacion del correo electronocio en el eCommerce'
            # Contenido en el cuerpo del correo electronico
            body = render_to_string('accounts/account_verification_email.html', {
                # Valores que se pintaran dinamicamente en el contenido
                # Data del usuario que se registro
                'user': user,
                # Dominio referido a la pagina actual
                'domain': current_site,
                # id para identificar al usuario a verificar
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            # Variabel que representara el email del cliente
            to_email = email
            # Variable objeto que procesara el correo electronico
            send_email = EmailMessage(
                # Email que se enviara
                mail_subject,
                # Contenido del email
                body,
                # A quien sera enviado
                to=[to_email]
            )
            # Envio del email
            send_email.send()

            # Mensaje de regsitro exitoso
            #messages.success(request, 'Se registro el usuario exitosamente')

            # Redirecciono al template de login y envio dos parametros, el command y el email
            return redirect('/accounts/login/?command=verification&email='+email)
    # Variable Json con las propiedades para el formulario
    context = {
        'form': form
    }
    # Retorno del request y Json a el template account/register.html
    return render(request, 'accounts/register.html', context)

# Metodo def para la ejecucion de la logica correspondiente al logeo de los usuarios
def login(request):
    # Valido que el request contenga un post en el body
    if request.method == 'POST':
        # Extraigo los valores de email y password
        email = request.POST['email']
        password = request.POST['password']

        # Proceso de authenticacion
        user = auth.authenticate(
            # Parametro necesarios para la authenticacion del usuario
            email=email, password=password
        )

        # Valido que el objeto user no sea nullo
        if user is not None:
            try:
                # Busqueda del carrito de compras
                cart = Cart.objects.get(cart_id=_cart_id(request))
                # Busco si el carrto de compras tiene productos agregados
                is_cart_item_exist = CartItem.objects.filter(
                    cart=cart).exists()
                # En caso de que si existan productos en carrito de compras, traigo los productos en un arreglo
                if is_cart_item_exist:
                    # Creo un arreglo con los productos del carrito de compras
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Logica para compara los variations de los nuevos productos con los productos ya existetes

                    # Variations de los productos con el usuario estando no en sesion
                    product_variations = []
                    for item in cart_item:
                        variations = item.variations.all()
                        product_variations.append(list(variations))

                    # Variations de los productos cuando el usuario esta en sesion
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variations = item.variations.all()
                        ex_var_list.append(list(existing_variations))
                        id.append(item.id)

                    # Extraccion de los valores coincidentes de las listas product_variations y ex_var_list
                    # Creo un objeto por cada elmento de la lista product_variations
                    for pr in product_variations:
                        # Comparo el objeto con los elemntos de la lista ex_var_list
                        if pr in ex_var_list:
                            # Extraigo el elemeto que coincide con el objeto pr
                            index = ex_var_list.index(pr)
                            # Extraigo el id del objeto pr
                            item_id = id[index]
                            # Busco el registro en la tabla CartItem usando como parametro el item_id
                            item = CartItem.objects.get(id=item_id)
                            # Incremento a uno el valor de la propiedad quantity del producto extraido de la tabla CartItem
                            item.quantity += 1
                            # Ligo el producto al usuario en sesion
                            item.user = user
                            # Guardo los cambios
                            item.save()
                        # Si el objeto pr no coicide con ningun elmento de la lista ex_var_list
                        else:
                            # Traigo todos lo productos del cart
                            cart_item = CartItem.objects.filter(cart=cart)
                            # Creo un objeto por cada elemto de la lista cart_item
                            for item in cart_item:
                                # Ligo los productos del cart al usuario en sesion
                                item.user = user
                                # Guardo los cambios
                                item.save()
            except:
                pass

            # Ejecuto el metodo login con la data del usuario registrado
            auth.login(request, user)
            messages.success(request, 'Has iniciado sesion exitosamente')

            # Captura de la url
            url = request.META.get(
                # Captura de la futura url
                'HTTP_REFERER'
            )
            # Captura del parametro ?next del url
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)
            except:
                return redirect('dashboard')

        else:
            # Envio un mensaje indicando que el emial o password son incorrectos
            messages.error(request, 'Las credenciales son incorrectas')
            return redirect('login')

    return render(request, 'accounts/login.html')

# Sentecia que permitira que el metodo logout solo se ejecute cuando el usuario esta en sesion
@login_required(login_url='login')
# Metodo def para la ejecucion de la logica correspondiente del cierre de session de los usuarios.
def logout(request):
    # Metedo para salir de la session
    auth.logout(request)
    # Mensaje de salida de session
    messages.success(request, "Has salido de sesion exitosamente")
    return redirect('login')

# Metodo para la activacion del usuario
def activate(request, uidb64, token):
    try:
        # Desencriptacion del primary key del usuario
        uid = urlsafe_base64_decode(uidb64).decode()
        # Busqueda del usuario en base de datos usando como filtro el pk
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Evaluo si el user no esta vacio y si el token tiene un valor
    if user is not None and default_token_generator.check_token(user, token):
        # Cambio el estado de la propiedad is_active a True
        user.is_active = True
        # Guardo los cambios en base de datos
        user.save()
        # Imprimo un mensaje de activacion exitosa
        messages.success(request, 'Felicidades, tu cuenta esta activa!')
        # Redirecciono a Login.html
        return redirect('login')
    else:
        messages.error(request, 'La activacion es invalida')
        return redirect('register')

# Metodo para ejecitar el template dashboard
# Este metodo solo sera accesible para los usuarios que esten logiados
@login_required(login_url='login')
def dashboard(request):
    # Extraccion de las ordenes de manera acendente del usuario en sesion
    orders = Order.objects.order_by(
        '-created_at').filter(user_id=request.user.id, is_ordered=True)

    # Extraccion de la cantidad de ordenes
    orders_count = orders.count()

    #Extraccion del perfil del usuario
    userprofile = UserProfile.objects.get(user_id = request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile
    }
    # Objeto Json con la data que sera enviada al template dashboard.html
    return render(request, 'accounts/dashboard.html', context)

# Metodo para enviar el email de la restauracion del password
def forgotPassword(request):
    # Validacion del metodo dentro del request
    if request.method == 'POST':
        # Extraccion del email
        email = request.POST['email']
        # Busco el registro que councuerde con el email
        if Account.objects.filter(email=email).exists():
            # Objetengo el usuario de la base de datos
            user = Account.objects.get(email__exact=email)

            # Creacion del correo que se enviara para la restauracion del password

            # Dominio
            current_site = get_current_site(request)
            # Titulo del correo
            mail_subject = 'Resetauracion del Paasword'
            # Cuerpo del correo
            body = render_to_string('accounts/reset_password_email.html', {
                # Data del usuario
                'user': user,
                # Dominio de la restauracion
                'domain': current_site,
                # PK del usuario encriptada
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # Token creado de manera exclusiva para este usuario
                'token': default_token_generator.make_token(user)
            })

            # Variable con el email al que se enviara
            to_email = email
            # Objeto con la estructura del correo
            send_email = EmailMessage(
                # Titulo del correo
                mail_subject,
                # Cuerpo del correo
                body,
                # A quien sera enviado
                to=[to_email]
            )
            # Envio del correo
            send_email.send()

            # Mensaje de confirmacion
            messages.success(
                request, 'Un email fuen enviado a tu bandeja de entrada para restaurar tu password')

            return redirect('login')
        # En caso de que no exista el usuario en la base de datos, muestro un mensaje de error y redirecciono a forgotPassword
        else:
            messages.error(request, 'La cuenta de usuario no existe')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')

# Metodo de la restauracion del password
def resetpassword_validate(request, uidb64, token):
    # Desincriptacion del pk del usuario
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        # Obtencion del usuario con el pk como filtro
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Validacion del objeto user
    if user is not None and default_token_generator.check_token(user, token):
        # otorgo el valor del uid a la propiedad uid de la session en el request
        request.session['uid'] = uid
        # Mensaje que pedira al usuario cambiar el password
        messages.success(request, 'Por favor resetea tu password')
        # Template con el formualario de restauracion
        return redirect('resetPassword')
    # En caso de que el link ya este expirdo
    else:
        messages.error(request, 'El link ha expirado')
        return redirect('login')

# Funcion de procesamiento del formulario para restaurar password
def resetPassword(request):
    # Valido que el request tenga un metodo POST en el body
    if request.method == 'POST':
        # Extraigo los valores de las propiedades password y confirm_password de el body del request
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Valido que el password y confirm_password sean iguales
        if password == confirm_password:
            # Extraigo el pk del usuaario que se encuentra en la propiedad id del request.session
            uid = request.session.get('uid')
            # Busco el registro del usuario usando como filtro la variable uid
            user = Account.objects.get(pk=uid)
            # Cambio el valor de la propiedad password por el valor de la variable password
            user.set_password(password)
            # Guardo los cambios en la base de datos
            user.save()
            # Muestro un mensaje de exito al usuario
            messages.success(request, 'El password se reseteo correctamente')
            # Redirecciono al usuario al login
            return redirect('login')
        # En caso de que el password y confirm_password no sean iguales
        else:
            # Muestro un mensaje al usuario de que los password no concuerdan.
            messages.error(request, 'El password de confirmacion no concuerda')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url = 'login')
def edit_profile(request):
    # Extraccion del registro de la tabla UserProfile con la data del usuario
    userprofile = get_object_or_404(UserProfile, user=request.user)

    # Evalucion del metodo post en el request
    if request.method == 'POST':
        # Match de la data request.user con el formulario UserForm
        user_form = UserForm(request.POST, instance=request.user)
        
        # Match de la data de userprofile con el formulario de UserProfileForm
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)

        # Si los formualario matcheados son validos, los alamceno en base de datos.
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Su informacion fue guardada con exito')
            return redirect('edit_profile')
            
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile': userprofile,
        }

        return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url = 'login')
#Metodo para el reseteo de password
def change_password(request):
    #Valido que el metodo en el interior del request sea de tipo POST
    if request.method == 'POST':
        #Extraigo los valores necesarios para el cambio de password
        current_password = request.POST['current_password']
        new_password = request.POST['new-password']
        confirm_password = request.POST['confirm_password']

        #Busco el usuario en la tabla Accounts
        user = Account.objects.get(username__exact = request.user.username)

        #Valido que el password coincida con new_password y confirm_password
        if new_password == confirm_password:
            #Hago el cambio de password al registro del usuario en la base de datos.
            success = user.check_password(new_password)
            if success:
                user.set_password(new_password)
                user.save()
            
                #Mensaje de exito
                messages.success(request, 'El password se actualizo exiosamente')
                return redirect('change_password')
            else:
                messages.error(request, 'Por favor ingrese un password valido ')
                return redirect('change_password')
        else:
            messages.error(request, 'Los passwords no coinciden, intente otra vez')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')