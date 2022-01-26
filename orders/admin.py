from django.contrib import admin
from .models import Payment, Order, OrderProducts
# Register your models here.

#Clase que me permitira ver los productos ligados a la orden del usuario
class OrderProductInline(admin.TabularInline):
    #modelo que se usara
    model = OrderProducts
    #Campos de lectura dentro de la tabla
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


#Clase que pintara las propiedades en el grid de Order
class OrderAdmin(admin.ModelAdmin):
    #Lista con las columnas que se mostraran en el grid de Django
    list_display = ['order_number', 'full_name', 'phone', 'emails', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    #Filtros de la data dentro del Grid
    list_filter = ['status', 'is_ordered']
    #Filtros de busqueda
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'emails']
    #Indicacion de cuantos records se imprimiran en el Grid
    list_per_page = 20
    #Campos que se mostraran como una tabla
    inlines = [ OrderProductInline]

#Registro de los models para la interfaz Django
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProducts)
