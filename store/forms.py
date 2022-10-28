from django import forms
from .models import ReviewRating, Product

class ReviewForm(forms.ModelForm):

    class Meta:
        #Entidad de la que se basara el formulario
        model = ReviewRating
        #Campos que contendra el formulario
        fields = ['subject', 'review', 'rating']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','decription','images','category','price','stock']
        excluide = ['slug',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })