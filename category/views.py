from ast import Return
from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm
import re
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def new_category(request):
    if request.user.is_admin == False:
        messages.warning(request, 'NO TIENES ACCESO A ESTE NIVEL')
        return render(request, 'accounts/dashboard.html')
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            description = form.cleaned_data['description']
            cat_image = form.cleaned_data['cat_image']
            sin_caracters = re.sub(r"[^\w\s]", '', category_name)
            slug = re.sub(r"\s+", "-", sin_caracters)

            category = Category.objects.create(category_name=category_name, description=description, cat_image=cat_image, slug=slug.lower())
            category.save()
            messages.success(request, 'La categoria ' + category_name + ' se ha creado exitosamente.')

    context = {
        'form': form
    }

    return render(request, 'category/nueva_categoria.html', context)
