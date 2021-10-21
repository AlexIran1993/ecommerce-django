from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

#Clase que creara a los usuarios y superusuarios
class MyAccountManager(BaseUserManager):
    #Metodo para crear los usuarios
    def create_user(self, first_name, last_name, username, email, password = None):
        #En caso de no existir el parametro email, lanzo un error
        if not email: 
            raise ValueError('el usuario debe tener un email')
        
        #En caso de no tener un username, se lanza un error
        if not username:
            raise ValueError('El usuario debe tener un username')

        #Creacion del user con la data que llega como parametro
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        #Cracion del password 
        user.set_password(password)
        #Guardoi en base de datos el usuario que se acaba de crear
        user.save(using = self._db)
        #Retorno el usuario que se acaba de crear.
        return user

    #Funcion usada para crear un superusuario
    def create_superuser(self, first_name, last_name, email, username, password):
        #Creacion del usuario
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )

        #Seteo de los atributos del admin
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        #Guardo el record
        user.save(using = self._db)
        return user


#Clase de identidad para la app de account que se extendera hasta AbstractBaseUser
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_numer = models.CharField(max_length=50)

    #Campos atributos de django
    #Campo de fecha de creacion
    date_joined = models.DateTimeField(auto_now_add=True)
    #Campo ultimo inicio de secion
    last_login = models.DateTimeField(auto_now_add=True)
    #Campo de identificacion para administradores
    is_admin = models.BooleanField(default=False)
    #Campo de identificacion para saber si es parte del staff de ventas
    is_staff = models.BooleanField(default=False)
    #Campo para saber si es un superAdmin
    is_superadmin = models.BooleanField(default=False)

    #Inicio de sesion usando el email
    USERNAME_FIELD = 'email'
    #Campos obligatorios para el inicio de sesion
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #Intanciamiento de la clase MyAccountManager()
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    #Permiso para acceder como administrador
    def has_perm(self, perm, obj=None):
        #Este def se ejecutara en caso de que is_admin sea true.
        return self.is_admin
    
    #En caso de ser administrador que tenga acceso a los modulos
    def has_module_perms(self, add_label):
        return True
