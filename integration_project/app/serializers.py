from rest_framework import serializers
from app.models import Commodity, Conflict

class ConflictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conflict
        fields = '__all__'
        
    
class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'


class CommodityPriceSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    price = serializers.FloatField(allow_null=True)

class ConflictYearlySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    total = serializers.IntegerField()

class ConflictIntensitySerializer(serializers.Serializer):
    year = serializers.IntegerField()
    intensity_level = serializers.IntegerField()
    count = serializers.IntegerField()


class ConflictTypeSerializer(serializers.Serializer):
    type_of_conflict = serializers.IntegerField()
    total = serializers.IntegerField()