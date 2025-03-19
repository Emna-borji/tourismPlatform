from django.db import models

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
        db_table = 'archaeological_sites'  # Ensure it matches the table name in PostgreSQL
        managed = False  # Django won't modify the existing table (change to `True` if needed)

    def __str__(self):
        return self.name
    


class Festival(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)  # Assuming this stores an image URL
    date = models.DateField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'festival'  # Ensure it matches the table name in PostgreSQL
        managed = False  # Django won’t modify the existing table

    def __str__(self):
        return self.name



class GuestHouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    images = models.TextField(null=True, blank=True)  # Stores multiple image URLs as text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'guest_house'  # Matches PostgreSQL table name
        managed = False  # Prevents Django from altering the existing table

    def __str__(self):
        return self.name if self.name else "Guest House"
    


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
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'hotel'  # Matches PostgreSQL table name
        managed = False  # Prevents Django from altering the existing table

    def __str__(self):
        return self.name
    


class Museum(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    hours = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'museum'  # Matches PostgreSQL table name
        managed = False  # Prevents Django from altering the existing table

    def __str__(self):
        return self.name
