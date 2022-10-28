"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

#Packetes necesarios para el manedo de mediafiles
from django.conf.urls.static import static
from django.conf import settings

#Arreglo de paths con las diferentes apps que componnen al eCommerce
urlpatterns = [
    path('securelogin/', admin.site.urls),
    path('category/', include('category.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    #Path para señalar la pagina de inicio
    path(
        #Indicacion que este path sera para la pagina de inicio
        '',
        #Metodo def que se ejecutara en el archvio views
        views.home,
        #Nombre con el que señalare al path
        name="home"
    ),
    #Path para la redireccion de la app store
    path('store/', include('store.urls')),
    #Path para la redireccion a la app carts carts
    path('carts/', include('carts.urls')),
    #Path para la redireccion de la app account.
    path('accounts/', include('accounts.urls')),
    #Path para la redireccion a la app de orders
    path('orders/', include('orders.urls')),
    #Lectura de las variables mediafile desde el static
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
