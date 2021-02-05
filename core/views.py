from django.http import HttpResponse


def index(request):
    return HttpResponse(
        """
        <h1>Bienvenue sur Open Collectivités!</h1>
        <p>La documentation de l’API se trouve sur la page <a href="api/docs">/api/docs</a> 
        """
    )
