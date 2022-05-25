from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

'''
Each trip will have an instance of Trip model.
'''


class Trip(models.Model):
    CURRENCIES = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('AZN', 'AZN'),
    )
    trip_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trip_title = models.CharField(max_length=200)
    people_included = ArrayField(ArrayField(models.CharField(max_length=50)))  # To represent each person seperately
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.FloatField()
    currency = models.CharField(max_length=4, choices=CURRENCIES, default='USD')
    description = models.CharField(null=True, max_length=200)

    def __str__(self):
        return self.trip_title

    class Meta:
        ordering = ['start_date']  # Trips which will happen sooner will appear first


'''
 City model is created to manage cities separately. Connected to Trip model with trip_id foreign key
'''


class City(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=75)

    def __str__(self):
        return self.city_name
