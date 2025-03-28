from rest_framework import serializers
from .models import Hotel,Restaurant,Activity,Museum,ArchaeologicalSite,Festival,GuestHouse,Destination,Review

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'  # Include all fields


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class MuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Museum
        fields = '__all__'


class ArchaeologicalSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchaeologicalSite
        fields = '__all__'

class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival
        fields = '__all__'


class GuestHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestHouse
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'entity_type', 'entity_id', 'user', 'rating', 'comment', 'image', 'created_at', 'updated_at']
