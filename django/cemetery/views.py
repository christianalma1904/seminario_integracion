from rest_framework import viewsets
from rest_framework.permissions import AllowAny   
from .models import Sector, Grave, Deceased
from .serializers import SectorSerializer, GraveSerializer, DeceasedSerializer


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [AllowAny]              

class GraveViewSet(viewsets.ModelViewSet):
    queryset = Grave.objects.all()
    serializer_class = GraveSerializer
    permission_classes = [AllowAny]              


class DeceasedViewSet(viewsets.ModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer
    permission_classes = [AllowAny]             
