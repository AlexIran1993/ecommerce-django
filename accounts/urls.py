from django.urls import path
from . import views

urlpatterns = [
    # Path para el registro de un usuario
    path('register/', views.register, name='register'),
    # Path para el login del usuario
    path('login/', views.login, name='login'),
    # Path para el logout
    path('logout/', views.logout, name='logout'),
    # Path para la activacion del usuario
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # Path para ejecutar el metodo dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # Path inicial de accounts.
    path('', views.dashboard, name='dashboard'),
    # Path para enviar el correo con el link de reseteo de password
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    # Path que envia al usuario al formulario de reseteo de password
    path('resetpassword_validate/<uidb64>/<token>/',
         views.resetpassword_validate, name='resetpassword_validate'),
    # Path que ejecuta la logica para cambiar el valord el password
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    # Path que ejecuta el grid de las ordenes compradas por el cliente
    path('my_orders/', views.my_orders, name='my_orders'),
    # Path que ejecutara el template de edicion de perfil del usuario
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    #Path para el reseteo de password
    path('change_password/', views.change_password, name='change_password'),
]
