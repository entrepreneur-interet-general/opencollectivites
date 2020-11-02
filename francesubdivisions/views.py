from francesubdivisions.models import Region, Departement, Epci, Commune
from francesubdivisions.serializers import (
    RegionSerializer,
    DepartementSerializer,
    EpciSerializer,
    CommuneSerializer,
)
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    """
    The root of the api for France Subdivisions
    """
    return Response(
        {
            "regions": reverse("region-list", request=request, format=format),
            "departements": reverse("departement-list", request=request, format=format),
            "epci": reverse("epci-list", request=request, format=format),
            "communes": reverse("commune-list", request=request, format=format),
        }
    )


class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DepartementList(generics.ListCreateAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DepartementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EpciList(generics.ListCreateAPIView):
    queryset = Epci.objects.all()
    serializer_class = EpciSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EpciDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Epci.objects.all()
    serializer_class = EpciSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommuneList(generics.ListCreateAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommuneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
