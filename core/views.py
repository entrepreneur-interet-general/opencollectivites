from django.http import HttpResponse


def index(request):
    return HttpResponse("Bienvenue sur le projet Open Collectivités!")
