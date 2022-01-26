from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.

# Clase


class AccountAdmin(UserAdmin):
    # Priopiedades que quiero que se muetren el el grid de django
    list_display = (
        # Email del usuario
        'email',
        # Nombres del usuario
        'first_name',
        # Apellidos
        'last_name',
        'username',
        # Ultima conexion del usuario
        'last_login',
        # Fecha de creacion
        'date_joined',
        # Es activo
        'is_active'
    )

    # Almacenamiento del detalle del usuario
    list_display_links = ('email', 'first_name', 'last_name')
    # Campos de lectura de la ultima de fecha de conexion y fecha de creacion
    readonly_fields = ('last_login', 'date_joined')
    # Organizacion de forma acendente de la fecha de creacion del usuario
    ordering = ('date_joined',)

    # Iniciacion de variables
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Clase que adminstrar la clase UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    # Contro que me permita manejar las imagenes de Django
    def thumbnails(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%" >'.format(object.profile_picture.url))

    thumbnails.short_description = 'Imagen de Perfil'
    list_display = ('thumbnails', 'user', 'city', 'state', 'country')


# Registro de la clase Account como parte del django framework
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
