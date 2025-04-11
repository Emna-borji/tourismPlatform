from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator, RegexValidator


# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    hotel = models.BooleanField(default=False)  # New column to indicate if it's a hotel
    guest_house = models.BooleanField(default=False)  # New column to indicate if it's a guest house

    class Meta:
        db_table = 'equipment'
        managed = False  # Let PostgreSQL manage the table structure

    def __str__(self):
        return f"{self.name} (Hotel: {self.hotel}, Guest House: {self.guest_house})"




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
    


# class Restaurant(models.Model):
#     id = models.AutoField(primary_key=True)  # Primary key, auto-incrementing
#     name = models.CharField(
#         max_length=255, 
#         null=True, 
#         blank=True,
#         validators=[RegexValidator(r'^[a-zA-Z0-9\-\' ]*$', 'Name must contain only letters, numbers, spaces, dashes, and apostrophes.')]
#     )
#     forks = models.IntegerField(
#         validators=[
#             MinValueValidator(1, message="Forks must be at least 1."),
#             MaxValueValidator(5, message="Forks cannot be more than 5.")
#         ]
#     )
#     category = models.CharField(max_length=255, null=True, blank=True)  # Optional VARCHAR(255) field
#     description = models.TextField(null=True, blank=True)  # Optional Text field
#     price = models.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         null=True, 
#         blank=True, 
#         validators=[MinValueValidator(0.01, 'Price must be greater than zero')]
#     )
#     image = models.CharField(max_length=255, null=True, blank=True)  # Optional image field
#     phone = models.CharField(
#         max_length=50, 
#         null=True, 
#         blank=True,
#         validators=[RegexValidator(r'^\+?[0-9]*$', 'Phone number must be numeric and can optionally start with a "+"')]
#     )
#     site_web = models.CharField(max_length=255, null=True, blank=True)  # Optional website URL field
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
#                                    validators=[MinValueValidator(-90), MaxValueValidator(90)])
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
#                                     validators=[MinValueValidator(-180), MaxValueValidator(180)])
#     destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)


#     class Meta:
#         db_table = 'restaurant'  # Specify the exact table name in PostgreSQL
#         app_label = 'tourism'  # Link to your 'tourism' app
#         managed = False

#     def __str__(self):
#         return self.name
    
#     @staticmethod
#     def get_governorate(lat, lon):
#         """Fetch the governorate name from OpenStreetMap API."""
#         if lat is None or lon is None:
#             return None  # Avoid making API calls if coordinates are missing

#         url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
#         headers = {
#             "Accept-Language": "fr",  # Get response in French
#             "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
#         }

#         try:
#             response = requests.get(url, headers=headers, timeout=5)
#             response.raise_for_status()  # Raise error if the request fails
#             data = response.json()
#             return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
#         except requests.RequestException as e:
#             print(f"Error fetching governorate: {e}")
#             return None

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         """Automatically set the destination before saving the restaurant."""
#         governorate = self.get_governorate(self.latitude, self.longitude)
#         if governorate:
#             # Normalize governorate name
#             normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

#             # Search for the corresponding destination
#             destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

#             if destination:
#                 self.destination = destination
#             else:
#                 print(f"Destination not found for governorate: {governorate}")

#         super().save(*args, **kwargs)


class ActivityCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'activity_category'
        app_label = 'tourism'
        managed = False  # since the table already exists in the DB

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'cuisine'  # Link to the existing table
        managed = False  # Important if the table is already created manually in the DB

    def __str__(self):
        return self.name



class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9\-\' ]*$', 'Name must contain only letters, numbers, spaces, dashes, and apostrophes.')]
    )
    
    forks = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Forks must be at least 1."),
            MaxValueValidator(3, message="Forks cannot be more than 3.")  # matches your table constraint
        ]
    )
    
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01, 'Price must be greater than zero')]
    )
    
    image = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^\+?[0-9]*$', 'Phone number must be numeric and can optionally start with a "+"')]
    )
    
    site_web = models.CharField(max_length=255, null=True, blank=True)
    
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    address = models.TextField(blank=True, null=True)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    cuisine = models.ForeignKey(
        'Cuisine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'restaurant'
        app_label = 'tourism'
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
        self.full_clean()
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
        


# class Activity(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(
#         max_length=255, 
#         null=True, 
#         blank=True,
#         validators=[RegexValidator(r'^[a-zA-Z0-9\-\' ]*$', 'Name must contain only letters, numbers, spaces, dashes, and apostrophes.')]
#     )
#     category = models.CharField(max_length=255, blank=True, null=True)
#     price = models.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         null=True, 
#         blank=True, 
#         validators=[MinValueValidator(0.01, 'Price must be greater than zero')]
#     )
#     description = models.TextField(blank=True, null=True)
#     site_web = models.CharField(max_length=255, blank=True, null=True)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
#                                    validators=[MinValueValidator(-90), MaxValueValidator(90)])
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
#                                     validators=[MinValueValidator(-180), MaxValueValidator(180)])
#     image_url = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)  # Default to `CURRENT_TIMESTAMP`
#     updated_at = models.DateTimeField(auto_now=True)  # Will auto-update on changes
#     destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

#     class Meta:
#         db_table = 'activity'  # Matches the table name in PostgreSQL
#         managed = False  # Django won't modify the existing table (change to `True` if needed)

#     def __str__(self):
#         return self.name if self.name else "Unnamed Activity"
    
#     @staticmethod
#     def get_governorate(lat, lon):
#         """Fetch the governorate name from OpenStreetMap API."""
#         if lat is None or lon is None:
#             return None  # Avoid making API calls if coordinates are missing

#         url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
#         headers = {
#             "Accept-Language": "fr",  # Get response in French
#             "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"  # Required User-Agent
#         }

#         try:
#             response = requests.get(url, headers=headers, timeout=5)
#             response.raise_for_status()  # Raise error if the request fails
#             data = response.json()
#             return data.get('address', {}).get('state', "Inconnu")  # Get 'state' field
#         except requests.RequestException as e:
#             print(f"Error fetching governorate: {e}")
#             return None

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         """Automatically set the destination before saving the activity."""
#         governorate = self.get_governorate(self.latitude, self.longitude)
#         if governorate:
#             # Normalize governorate name
#             normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

#             # Search for the corresponding destination
#             destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

#             if destination:
#                 self.destination = destination
#             else:
#                 print(f"Destination not found for governorate: {governorate}")

#         super().save(*args, **kwargs)


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9\-\' ]*$', 'Name must contain only letters, numbers, spaces, dashes, and apostrophes.')]
    )


    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01, 'Price must be greater than zero')]
    )

    description = models.TextField(blank=True, null=True)
    site_web = models.CharField(max_length=255, blank=True, null=True)
    
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    image_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    destination = models.ForeignKey('Destination', on_delete=models.SET_NULL, null=True, blank=True, db_column='destination_id')

    class Meta:
        db_table = 'activity'
        managed = False

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
        self.full_clean()
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
    name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9\-\' ]*$', 'Name must contain only letters, numbers, spaces, dashes, and apostrophes.')]
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    period = models.CharField(max_length=100, blank=True, null=True)
    site_type = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
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
        self.full_clean()
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
    # Name with regex validator: only letters, numbers, spaces, dashes, and apostrophes
    name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9\-\' ]*$', 'Name must contain only letters, numbers, spaces, dashes, and apostrophes.')]
    )
    description = models.TextField()
    image = models.CharField(max_length=255)  # Assuming this stores an image URL
    date = models.DateField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0.01, 'Price must be greater than zero')]
    )
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
        self.full_clean()
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
    CATEGORY_CHOICES = [
        ('Basique', 'Basique'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
        ('Luxe', 'Luxe'),
    ]
    id = models.AutoField(primary_key=True)
    # Name with regex validator: only letters, numbers, spaces, dashes, and apostrophes
    name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9\-\' ]*$', 'Name must contain only letters, numbers, spaces, dashes, and apostrophes.')]
    )
    
    # Category (Choices with default value)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Standard')
    
    # Description (optional)
    description = models.TextField(null=True, blank=True)
    
    # Phone with custom regex validator for phone number format
    phone = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        validators=[RegexValidator(r'^\+?[0-9]*$', 'Phone number must be numeric and can optionally start with a "+"')]
    )
    
    # Email field with built-in Django EmailField validator
    email = models.EmailField(max_length=100, null=True, blank=True)
    
    # Website URL
    
    website = models.CharField(max_length=255, null=True, blank=True,
                               validators=[URLValidator(message="Enter a valid website URL.")])
    
    equipments = models.ManyToManyField(Equipment, related_name="guest_houses", blank=True)

    
    # Latitude and Longitude as floats
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
    
    # Images stored as text (list of URLs)
    images = models.TextField(null=True, blank=True)
    
    # Price with a custom validator to ensure it's a positive number
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0.01, 'Price must be greater than zero')]
    )
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
        self.full_clean()
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
    name = models.CharField(max_length=255,
                            validators=[RegexValidator(regex=r'^[A-Za-z0-9\s]+$', message="Hotel name should contain only letters and numbers.")])
    stars = models.IntegerField(null=True, blank=True,
                                validators=[MinValueValidator(1), MaxValueValidator(5)]  # Ensures stars are between 1 and 5
                                )
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                validators=[MinValueValidator(0)]  # Prevents negative prices
                                )
    image = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True,
                             validators=[RegexValidator(regex=r'^\+?[0-9]+$', message="Invalid phone number format.")])
    website = models.CharField(max_length=255, null=True, blank=True,
                               validators=[URLValidator(message="Enter a valid website URL.")])
    
    equipments = models.ManyToManyField(Equipment, related_name="hotels", blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
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
        """Ensure data consistency before saving the hotel."""
        if self.price is not None and self.price < 0:
            raise ValueError("Price cannot be negative.")

        if self.stars is not None and (self.stars < 1 or self.stars > 5):
            raise ValueError("Stars must be between 1 and 5.")

        if self.phone and not self.phone.isdigit():
            raise ValueError("Phone number should contain only digits.")
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


# class Hotel(models.Model):
#     name = models.CharField(
#         max_length=255,
#         validators=[RegexValidator(regex=r'^[A-Za-z0-9\s]+$', message="Hotel name should contain only letters and numbers.")]
#     )
#     stars = models.IntegerField(
#         null=True, blank=True,
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#     description = models.TextField(null=True, blank=True)
#     price = models.DecimalField(
#         max_digits=10, decimal_places=2, null=True, blank=True,
#         validators=[MinValueValidator(0)]
#     )
#     image = models.CharField(max_length=255, null=True, blank=True)
#     phone = models.CharField(
#         max_length=20, null=True, blank=True,
#         validators=[RegexValidator(regex=r'^\+?[0-9]+$', message="Invalid phone number format.")]
#     )
#     website = models.CharField(
#         max_length=255, null=True, blank=True,
#         validators=[URLValidator(message="Enter a valid website URL.")]
#     )

#     equipments = models.ManyToManyField(Equipment, related_name="hotels", blank=True)


#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
#                                    validators=[MinValueValidator(-90), MaxValueValidator(90)])
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True,
#                                     validators=[MinValueValidator(-180), MaxValueValidator(180)])
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     destination = models.ForeignKey('Destination', on_delete=models.SET_NULL, null=True, blank=True)

#     class Meta:
#         db_table = 'hotel'

#     def __str__(self):
#         return self.name
    
#     def available_equipments(self):
#         return self.equipments.filter(suitable_for__in=["hotel", "Hôtel / Maison d'hôte"])

#     @staticmethod
#     def get_governorate(lat, lon):

#         if lat is None or lon is None:
#             return None

#         url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
#         headers = {
#             "Accept-Language": "fr",
#             "User-Agent": "smart_tourism/1.0 (emnaborji2578@gmail.com)"
#         }

#         try:
#             response = requests.get(url, headers=headers, timeout=5)
#             response.raise_for_status()
#             data = response.json()
#             return data.get('address', {}).get('state', "Inconnu")
#         except requests.RequestException as e:
#             print(f"Error fetching governorate: {e}")
#             return None

#     def save(self, *args, **kwargs):
#         # Remove duplicate validations here (handled in serializer)

#         # Automatically set the destination
#         governorate = self.get_governorate(self.latitude, self.longitude)
#         if governorate:
#             from tourism.models import Destination
#             normalized_governorate = governorate.replace("Gouvernorat ", "").strip()

#             destination = Destination.objects.filter(name__icontains=normalized_governorate).first()

#             if destination:
#                 self.destination = destination
#             else:
#                 print(f"Destination not found for governorate: {governorate}")
#         super().save(*args, **kwargs)




class Museum(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'^[A-Za-z0-9\s]+$', message="Hotel name should contain only letters and numbers.")]
    )
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    hours = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        validators=[RegexValidator(
            regex=r'\d{1,2}\s*(AM|PM)\s*-\s*\d{1,2}\s*(AM|PM)', 
            message="Hours must be in the format '9 AM - 5 PM'."
        )]
    )
    website = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,
        validators=[RegexValidator(
            regex=r'https?://[^\s]+', 
            message="Invalid website URL format."
        )]
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]  # Latitude should be between -90 and 90
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]  # Longitude should be between -180 and 180
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]  # Price must be non-negative
    )
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
        self.full_clean()
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
    


class Favorite(models.Model):
    # Choices for entity_type
    ENTITY_TYPES = [
        ('activity', 'Activity'),
        ('museum', 'Museum'),
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('guest_house', 'Guest House'),
        ('archaeological_site', 'Archaeological Site'),
        ('festival', 'Festival'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=30, choices=ENTITY_TYPES)
    entity_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'favorite'  # Explicitly set the table name
        unique_together = ('user', 'entity_type', 'entity_id')  # Unique constraint
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user.username} favorite - {self.entity_type} {self.entity_id}"
    
