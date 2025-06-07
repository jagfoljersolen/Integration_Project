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
    

