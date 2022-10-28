from datetime import datetime
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager, PermissionsMixin)
from location_field.models.plain import PlainLocationField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth

ACTION_CHOICES = (("Pickup", "Pickup"), ("Delivery", "Delivery"))
STATUS_CHOICES = [('Scheduled', 'Scheduled'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')]


def upload_to(instance, filename):
    return 'images/image_file'.format(filename=filename)


class Dispatch(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    # owner = models.ForeignKey('auth.User', related_name='dispatches', on_delete=models.CASCADE, default='')
    dispatch_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    tractor = models.CharField(max_length=20, null=True)
    pickup_location = PlainLocationField(null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='Scheduled', null=True)
    commodity = models.TextField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    pickup_arrival_date = models.DateTimeField(null=True)
    pickup_departure_date = models.DateTimeField(null=True)
    pickup_arrival = models.BooleanField(default=False, null=True)
    departure_from_pickup = models.BooleanField(default=False, null=True)

    delivery_location = PlainLocationField(null=True)
    delivery_arrival_date = models.DateTimeField(null=True)
    delivery_departure_date = models.DateTimeField(null=True)
    delivery_arrival = models.BooleanField(default=False, null=True)
    delivery_departure = models.BooleanField(default=False, null=True)
    pod = models.FileField(upload_to=upload_to, null=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    company = models.CharField(max_length=30)
    person = models.CharField(max_length=20, null=True)
    phone_no = models.IntegerField(null=True)
    weight = models.CharField(max_length=20, default='', null=True)
    packages = models.CharField(max_length=20, default='', null=True)
    shipper = models.CharField(max_length=100, default='', null=True)
    pickup = models.DateTimeField(null=True)
    delivery = models.DateTimeField(null=True)
    dispatch_id = models.ForeignKey(Dispatch, related_name='order', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
