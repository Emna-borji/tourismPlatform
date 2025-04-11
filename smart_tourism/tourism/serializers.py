from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator, RegexValidator
from .models import Hotel,Restaurant,Activity,Museum,ArchaeologicalSite,Festival,GuestHouse,Destination,Review,Favorite, Cuisine, ActivityCategory,Equipment


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'

class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ['id', 'name']


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name']

class HotelSerializer(serializers.ModelSerializer):
    equipments = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), many=True)

    name = serializers.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'^[A-Za-z0-9\s]+$', message="Hotel name should contain only letters and numbers.")]
    )
    stars = serializers.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)]
    )
    phone = serializers.CharField(
        max_length=20, required=False,
        validators=[RegexValidator(regex=r'^\+?[0-9]+$', message="Invalid phone number format.")]
    )
    website = serializers.CharField(
        max_length=255, required=False,
        validators=[URLValidator(message="Enter a valid website URL.")]
    )


    class Meta:
        model = Hotel
        fields = '__all__'  # Include all fields

    def validate_equipments(self, value):
        """
        Only allow equipments where hotel=True.
        """
        invalid = [eq for eq in value if not eq.hotel]
        if invalid:
            raise serializers.ValidationError(f"Some equipments are not valid for hotels: {[e.id for e in invalid]}")
        return value

    def validate_name(self, value):
        """Custom validation for hotel name."""
        if len(value) < 3:
            raise serializers.ValidationError("Hotel name must be at least 3 characters long.")
        return value

    def validate_price(self, value):
        """Custom validation for price."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stars(self, value):
        """Custom validation for stars."""
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Stars must be between 1 and 5.")
        return value
    
    def create(self, validated_data):
        equipments_data = validated_data.pop('equipments', [])
        hotel = Hotel.objects.create(**validated_data)
        
        # Add equipment to the guest house
        for equipment in equipments_data:
            hotel.equipments.add(equipment)

        return hotel

    def update(self, instance, validated_data):
        equipments_data = validated_data.pop('equipments', [])
        instance = super().update(instance, validated_data)

        # Clear current equipment assignments and add new ones
        instance.equipments.clear()
        for equipment_data in equipments_data:
            equipment = Equipment.objects.get(id=equipment_data['id'])  # Get the equipment by ID
            instance.equipments.add(equipment)

        instance.save()
        return instance


        


class RestaurantSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer()
    class Meta:
        model = Restaurant
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class MuseumSerializer(serializers.ModelSerializer):
    # Custom validation for latitude and longitude
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a non-negative value.")
        return value

    name = serializers.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'^[A-Za-z0-9\s]+$', message="Hotel name should contain only letters and numbers.")]
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)]
    )
    phone = serializers.CharField(
        max_length=20, required=False,
        validators=[RegexValidator(regex=r'^\+?[0-9]+$', message="Invalid phone number format.")]
    )
    website = serializers.CharField(
        max_length=255, required=False,
        validators=[URLValidator(message="Enter a valid website URL.")]
    )
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

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__' # Customize fields as per your model


class GuestHouseSerializer(serializers.ModelSerializer):
    equipments = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), many=True)

    def validate_equipments(self, value):
        """
        Only allow equipments where guest_house=True.
        """
        invalid = [eq for eq in value if not eq.guest_house]
        if invalid:
            raise serializers.ValidationError(f"Some equipments are not valid for guest houses: {[e.id for e in invalid]}")
        return value


    # Custom validation for latitude and longitude
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a non-negative value.")
        return value

    name = serializers.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'^[A-Za-z0-9\s]+$', message="Hotel name should contain only letters and numbers.")]
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)]
    )
    phone = serializers.CharField(
        max_length=20, required=False,
        validators=[RegexValidator(regex=r'^\+?[0-9]+$', message="Invalid phone number format.")]
    )
    website = serializers.CharField(
        max_length=255, required=False,
        validators=[URLValidator(message="Enter a valid website URL.")]
    )

    class Meta:
        model = GuestHouse
        fields = '__all__'

    def create(self, validated_data):
        equipments_data = validated_data.pop('equipments', [])
        guest_house = GuestHouse.objects.create(**validated_data)
        
        # Add equipment to the guest house
        for equipment in equipments_data:
            guest_house.equipments.add(equipment)

        return guest_house

    def update(self, instance, validated_data):
        equipments_data = validated_data.pop('equipments', [])
        instance = super().update(instance, validated_data)

        # Clear current equipment assignments and add new ones
        instance.equipments.clear()
        for equipment_data in equipments_data:
            equipment = Equipment.objects.get(id=equipment_data['id'])  # Get the equipment by ID
            instance.equipments.add(equipment)

        instance.save()
        return instance





class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'entity_type', 'entity_id', 'user', 'rating', 'comment', 'image', 'created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user', 'entity_type', 'entity_id', 'created_at', 'updated_at']
