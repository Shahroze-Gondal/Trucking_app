from datetime import datetime

from django.db import models
from location_field.models.plain import PlainLocationField


ACTION_CHOICES = (("Pickup", "Pickup"), ("Delivery", "Delivery"))
STATUS_CHOICES = [('Scheduled', 'Scheduled'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')]


def upload_to(instance, filename):
    return 'images/image_file'.format(filename=filename)


class Dispatch(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    dispatch_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    tractor = models.CharField(max_length=20)
    pickup_location = PlainLocationField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='Scheduled')
    commodity = models.TextField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    pickup_arrival_date = models.DateTimeField(null=True)
    pickup_departure_date = models.DateTimeField(null=True)
    pickup_arrival = models.BooleanField(default=False)
    departure_from_pickup = models.BooleanField(default=False)

    delivery_location = PlainLocationField()
    delivery_arrival_date = models.DateTimeField(null=True)
    delivery_departure_date = models.DateTimeField(null=True)
    delivery_arrival = models.BooleanField(default=False)
    delivery_departure = models.BooleanField(default=False)
    # pod = models.ImageField(upload_to=upload_to, blank=True)
    pod = models.TextField(blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    company = models.CharField(max_length=30)
    person = models.CharField(max_length=20)
    phone_no = models.IntegerField()
    weight = models.CharField(max_length=20, default='')
    packages = models.CharField(max_length=20, default='')
    shipper = models.CharField(max_length=100, default='')
    pickup = models.DateTimeField(null=True)
    delivery = models.DateTimeField(null=True,)
    dispatch_id = models.ForeignKey(Dispatch, related_name='order', on_delete=models.CASCADE)

    def __str__(self):
        return self.title