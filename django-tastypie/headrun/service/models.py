from django.db import models

# Create your models here
class Theaterservice(models.Model):
    sk = models.CharField(max_length=150, primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300, blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    firm_name = models.CharField(max_length=150, blank=True, null=True)
    no_of_rooms = models.IntegerField(default=0)
    no_of_seats = models.IntegerField(default=0)
    contact_numbers = models.CharField(max_length=250, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField(default=0.000)
    longitude = models.FloatField(default=0.000)
    address = models.TextField(blank=True, null=True)
    theater_url = models.TextField(blank=True)
    aux_info =  models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True)
    modified_at = models.DateTimeField()
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Theater'
