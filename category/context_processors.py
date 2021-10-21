from .models import Category

def menu_links(request):
    #Lista de links que provienen de la base de datos
    links = Category.objects.all()
    #Retorno un Json con la lista de links
    return dict(links = links)