from django import forms
from .models import Account, UserProfile

# Clase que contendra las propiedades para el registro de usuarios


class RegistrationForm(forms.ModelForm):

    # Cajas de texto para el password y la confirmacion del password
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # Atributos de la caja de texto
        'placeholder': 'Ingrese password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        # Atributos de la caja de texto
        'placeholder': 'Confirmar password',
        'class': 'form-control',
    }))

    class Meta:
        # Modelado basandode en la clase Account quien es quien tienen los campos de registro
        model = Account
        # Propiedades que tomare en cuenta del modelo Account para el registro de nuevos usuarios
        fields = ['first_name', 'last_name',
                  'phone_numer', 'email', 'password']

    # Asignacion de estilos a los campos
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese el nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['phone_numer'].widget.attrs['placeholder'] = 'Ingrese su numero telefonico'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese el email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # Funcion para validar que el password se el mismo
    def clean(self):
        # Obtengo acceso a los datos del formulario
        cleaned_data = super(RegistrationForm, self).clean()
        # Extraigo los valores de password y confirm_password
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        # Validacion de los passwords
        if password != confirm_password:
            raise forms.ValidationError(
                "El password no coincide"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_numer')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages= {'invalid': ('Solo archivos de imagen')}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

        def __init__(self, *args, **kwargs):
            super(UserProfileForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'