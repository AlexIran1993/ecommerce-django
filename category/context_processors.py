#Importacion de la clase Category.
from .models import Category

def menu_links(request):
    #Lista de las categorias registradas en base de datos.
    links = Category.objects.all()
    #Retorno un Json con la lista de categorias
    return dict(links = links)