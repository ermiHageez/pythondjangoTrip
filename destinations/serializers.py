from rest_framework import serializers
from .models import Destination, Package

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
class PackageSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    class Meta:
        model = Package
        fields = '__all__'