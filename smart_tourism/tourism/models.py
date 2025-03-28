from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from users.models import CustomUser



# Create your models here.



class Destination(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly set the primary key
    name = models.CharField(max_length=255)
    latitude = models.FloatField()  # Matches 'double precision' in PostgreSQL
    longitude = models.FloatField()  # Matches 'double precision' in PostgreSQL

    class Meta:
        db_table = 'destination'  # Explicitly specify schema
        app_label = 'tourism'
        managed = False

    def __str__(self):
        return self.name
    


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)  # Primary key, auto-incrementing
    name = models.CharField(max_length=255)  # VARCHAR(255) field
    forks = models.IntegerField()  # Integer field (with a range check in PostgreSQL)
    category = models.CharField(max_length=255, null=True, blank=True)  # Optional VARCHAR(255) field
    description = models.TextField(null=True, blank=True)  # Optional Text field
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Numeric field
    image = models.CharField(max_length=255, null=True, blank=True)  # Optional image field
    phone = models.CharField(max_length=200, null=True, blank=True)  # Optional phone field
    site_web = models.CharField(max_length=255, null=True, blank=True)  # Optional website URL field
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)  # Numeric field for latitude
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)  # Numeric field for longitude
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        db_table = 'restaurant'  # Specify the exact table name in PostgreSQL
        app_label = 'tourism'  # Link to your 'tourism' app
        managed = False

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_governorate(lat, lon):
        """Fetch the governorate name from OpenStreetMap API."""
        if lat is None or lon is None:
            return None  # Avoid making API calls if coordinates are missing

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {
            "Accept-Language": "fr",  # Get response in French
            "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()
            return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
        except requests.RequestException as e:
            print(f"Error fetching governorate: {e}")
            return None

    def save(self, *args, **kwargs):
        """Automatically set the destination before saving the restaurant."""
        governorate = self.get_governorate(self.latitude, self.longitude)
        if governorate:
            # Normalize governorate name
            normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

            # Search for the corresponding destination
            destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

            if destination:
                self.destination = destination
            else:
                print(f"Destination not found for governorate: {governorate}")

        super().save(*args, **kwargs)
        


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    site_web = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Default to `CURRENT_TIMESTAMP`
    updated_at = models.DateTimeField(auto_now=True)  # Will auto-update on changes
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'activity'  # Matches the table name in PostgreSQL
        managed = False  # Django won't modify the existing table (change to `True` if needed)

    def __str__(self):
        return self.name if self.name else "Unnamed Activity"
    
    @staticmethod
    def get_governorate(lat, lon):
        """Fetch the governorate name from OpenStreetMap API."""
        if lat is None or lon is None:
            return None  # Avoid making API calls if coordinates are missing

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {
            "Accept-Language": "fr",  # Get response in French
            "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()
            return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
        except requests.RequestException as e:
            print(f"Error fetching governorate: {e}")
            return None

    def save(self, *args, **kwargs):
        """Automatically set the destination before saving the activity."""
        governorate = self.get_governorate(self.latitude, self.longitude)
        if governorate:
            # Normalize governorate name
            normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

            # Search for the corresponding destination
            destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

            if destination:
                self.destination = destination
            else:
                print(f"Destination not found for governorate: {governorate}")

        super().save(*args, **kwargs)
    


class ArchaeologicalSite(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    period = models.CharField(max_length=100, blank=True, null=True)
    site_type = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)  # Assuming it's a URL or base64 string
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'archaeological_site'  # Ensure it matches the table name in PostgreSQL
        managed = False  # Django won't modify the existing table (change to `True` if needed)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_governorate(lat, lon):
        """Fetch the governorate name from OpenStreetMap API."""
        if lat is None or lon is None:
            return None  # Avoid making API calls if coordinates are missing

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {
            "Accept-Language": "fr",  # Get response in French
            "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()
            return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
        except requests.RequestException as e:
            print(f"Error fetching governorate: {e}")
            return None

    def save(self, *args, **kwargs):
        """Automatically set the destination before saving the archaeological site."""
        governorate = self.get_governorate(self.latitude, self.longitude)
        if governorate:
            # Normalize governorate name
            normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

            # Search for the corresponding destination
            destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

            if destination:
                self.destination = destination
            else:
                print(f"Destination not found for governorate: {governorate}")

        super().save(*args, **kwargs)
    


class Festival(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)  # Assuming this stores an image URL
    date = models.DateField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'festival'  # Ensure it matches the table name in PostgreSQL
        managed = False  # Django won’t modify the existing table

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_governorate(lat, lon):
        """Fetch the governorate name from OpenStreetMap API."""
        if lat is None or lon is None:
            return None  # Avoid making API calls if coordinates are missing

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {
            "Accept-Language": "fr",  # Get response in French
            "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()
            return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
        except requests.RequestException as e:
            print(f"Error fetching governorate: {e}")
            return None

    def save(self, *args, **kwargs):
        """Automatically set the destination before saving the festival."""
        governorate = self.get_governorate(self.latitude, self.longitude)
        if governorate:
            # Normalize governorate name
            normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

            # Search for the corresponding destination
            destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

            if destination:
                self.destination = destination
            else:
                print(f"Destination not found for governorate: {governorate}")

        super().save(*args, **kwargs)



class GuestHouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    images = models.TextField(null=True, blank=True)  # Stores multiple image URLs as text
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'guest_house'  # Matches PostgreSQL table name
        managed = False  # Prevents Django from altering the existing table

    def __str__(self):
        return self.name if self.name else "Guest House"
    
    @staticmethod
    def get_governorate(lat, lon):
        """Fetch the governorate name from OpenStreetMap API."""
        if lat is None or lon is None:
            return None  # Avoid making API calls if coordinates are missing

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {
            "Accept-Language": "fr",  # Get response in French
            "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()
            return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
        except requests.RequestException as e:
            print(f"Error fetching governorate: {e}")
            return None

    def save(self, *args, **kwargs):
        """Automatically set the destination before saving the guest house."""
        governorate = self.get_governorate(self.latitude, self.longitude)
        if governorate:
            # Normalize governorate name
            normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

            # Search for the corresponding destination
            destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

            if destination:
                self.destination = destination
            else:
                print(f"Destination not found for governorate: {governorate}")

        super().save(*args, **kwargs)

    


class Guide(models.Model):
    num_gd = models.AutoField(primary_key=True)
    descatl = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'guide'  # Matches PostgreSQL table name
        managed = False  # Prevents Django from altering the existing table

    def __str__(self):
        return self.name if self.name else "Guide"





class Hotel(models.Model):
    name = models.CharField(max_length=255)
    stars = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey('Destination', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'hotel'  # Matches PostgreSQL table name
        managed = False  # Prevents Django from altering the existing table

    def __str__(self):
        return self.name

    @staticmethod
    def get_governorate(lat, lon):
        """Fetch the governorate name from OpenStreetMap API."""
        if lat is None or lon is None:
            return None  # Avoid making API calls if coordinates are missing

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {
            "Accept-Language": "fr",  # Get response in French
            "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()
            return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
        except requests.RequestException as e:
            print(f"Error fetching governorate: {e}")
            return None

    def save(self, *args, **kwargs):
        """Automatically set the destination before saving the hotel."""
        governorate = self.get_governorate(self.latitude, self.longitude)
        if governorate:
            from tourism.models import Destination  # Import inside to avoid circular import issues
            
            normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

            destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

            if destination:
                self.destination = destination
            else:
                print(f"Destination not found for governorate: {governorate}")
        super().save(*args, **kwargs)



class Museum(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    hours = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'museum'  # Matches PostgreSQL table name
        managed = False  # Prevents Django from altering the existing table

    def __str__(self):
        return self.name
    

    @staticmethod
    def get_governorate(lat, lon):
        """Fetch the governorate name from OpenStreetMap API."""
        if lat is None or lon is None:
            return None  # Avoid making API calls if coordinates are missing

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        headers = {
            "Accept-Language": "fr",  # Get response in French
            "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()
            return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
        except requests.RequestException as e:
            print(f"Error fetching governorate: {e}")
            return None

    def save(self, *args, **kwargs):
        """Automatically set the destination before saving the museum."""
        governorate = self.get_governorate(self.latitude, self.longitude)
        if governorate:
            # Normalize governorate name
            normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

            # Search for the corresponding destination
            destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

            if destination:
                self.destination = destination
            else:
                print(f"Destination not found for governorate: {governorate}")

        super().save(*args, **kwargs)



class Review(models.Model):
    ENTITY_TYPES = [
        ('guest_house', 'Guest House'),
        ('restaurant', 'Restaurant'),
        ('hotel', 'Hotel'),
        ('museum', 'Museum'),
        ('festival', 'Festival'),
        ('activity', 'Activity'),
        ('archaeological_sites', 'Archaeological Sites'),
    ]
    
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPES)
    entity_id = models.IntegerField()  # ID of the related entity (e.g., restaurant or museum)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)  # If you store image URLs or base64 string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'review'
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1, rating__lte=5), name='rating_check'),
        ]

    def __str__(self):
        return f"Review by {self.user.username} for {self.entity_type} #{self.entity_id}"
    
    
