"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from ctypes import cast
from email.policy import default
from pathlib import Path
#Herramineta usada para la seguridad de los archivos publicos
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default = True)

#Host del seervidor AWS.
ALLOWED_HOSTS = ['http://ecommerce-env.eba-ixjnmvjx.us-west-2.elasticbeanstalk.com/']


# Application definition
#Lista de aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Registro de la app category
    'category',
    #Registro de la app de accounts
    'accounts',
    #Registro de la app de store
    'store',
    #Registro de la app de carts
    'carts',
    #Registro de la app de orders
    'orders',
    #Registro del honeypoy
    'admin_honeypot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

#Configuracino para finalizar la sessino en automatico
#Tiempo que tardara en expirar la sesion
SESSION_EXPIRE_SECONDS = 3600
#La session expirara cuando el usuario deje de interactura con la aplicacion
SESSION_EXPIRE_AFTER_LAS_ACTIVITY = True
#Pagina de redireccino cuando expire la sesion
SESSION_TIMEOUT_REDIRECT = 'accounts/login'

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #Lista de directorios de los templates
            'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #Registro de la funcion que almacena las categorias extraidas en context_processors.py
                #Nombre de la app / Nombre del archivo / Nombre de la funcion
                'category.context_processors.menu_links',
                #Registro de la funcion counters para saber la cantidad de productos que tiene el carrito
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

#Modelo de autenticacion para que reconozca a Account como clase principal para el almacenamiento de usuarios.
AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    'ecommerce/static'
]

#Direccion donde se almacenaran los archivos mediadile
MEDIA_ROOT = BASE_DIR / 'media'
#Variables usadas para los archivos mediafile
MEDIA_URL = '/media/'


#Libreria para la creacion de mensages de error personalizados.
from django.contrib.messages import constants as messages
MESSAGE_TAG = {
    messages.ERROR : 'danger',
}

#Configuracion para el uso de los servidores de gmail
EMAIL_HOST =config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
