# app/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Count

from .models import Conflict, Commodity
from .serializers import ConflictYearlySerializer, ConflictSerializer, ConflictTypeSerializer, CommoditySerializer

class ConflictYearlyDataAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conflicts = Conflict.objects.values('year').annotate(
            total=Count('conflict_id')
        ).order_by('year')

        serializer = ConflictYearlySerializer(conflicts, many=True)
        return Response({'yearly_data': serializer.data})

class ConflictListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Conflict.objects.all()
    serializer_class = ConflictSerializer

from django.db.models import Count

class ConflictIntensityDataApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        intensity_data = Conflict.objects.values('year', 'intensity_level').annotate(
            count=Count('conflict_id')
        ).order_by('year', 'intensity_level')

        return Response({'intensity_data': intensity_data})

    
class ConflictTypesDataApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conflict_types = Conflict.objects.values('type_of_conflict').annotate(
            total=Count('conflict_id')
        ).order_by('type_of_conflict')

        serializer = ConflictTypeSerializer(conflict_types, many=True)
        return Response({'conflict_types': serializer.data})

class CommodityListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        commodity_field = request.query_params.get('commodity')
        if not commodity_field:
            return Response({"error": "Missing 'commodity' parameter"}, status=400)

        try:
            # Check if the field exists on the model
            if not hasattr(Commodity, commodity_field):
                return Response({"error": f"Invalid commodity field: {commodity_field}"}, status=400)

            # Fetch all objects with a non-null value for this commodity
            commodities = Commodity.objects.exclude(**{f"{commodity_field}__isnull": True}).order_by('year')

            years = []
            prices = []

            for item in commodities:
                value = getattr(item, commodity_field)
                if value is not None:
                    years.append(item.year)
                    prices.append(value)

            if not years:
                return Response({"error": "No data found for this commodity."}, status=404)

            # You can map the field to a human-readable name if needed
            commodity_name = commodity_field.replace("_", " ").title()

            return Response({
                "commodity_name": commodity_name,
                "years": years,
                "prices": prices
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
