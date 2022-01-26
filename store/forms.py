from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):

    class Meta:
        #Entidad de la que se basara el formulario
        model = ReviewRating
        #Campos que contendra el formulario
        fields = ['subject', 'review', 'rating']