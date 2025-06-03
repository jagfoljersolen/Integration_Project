from rest_framework import generics
from app.models import Commodity, Conflict
from .serializers import CommoditySerializer, ConflictSerializer

class ConflictListView(generics.ListCreateAPIView):
    queryset = Conflict.objects.all()
    serializer_class = ConflictSerializer

class ConflictDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conflict.objects.all()
    serializer_class = ConflictSerializer

class CommodityListView(generics.ListCreateAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

class CommodityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer



