from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_24_hour_format
# Create your models here.

class User(AbstractUser):
    pass

class BusRoute(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class StopPoint(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PickupPoint(models.Model):
    bus_route = models.ForeignKey(BusRoute, related_name="pickup_points", on_delete=models.CASCADE)
    stop_point = models.ForeignKey(StopPoint, on_delete=models.CASCADE)
    time = models.CharField(max_length=4, validators=[validate_24_hour_format], blank=True, null=True)

    def __str__(self):
        return f"Pickup at {self.stop_point.name} for {self.bus_route.name} at {self.time}"

class DropPoint(models.Model):
    bus_route = models.ForeignKey(BusRoute, related_name="drop_points", on_delete=models.CASCADE)
    stop_point = models.ForeignKey(StopPoint, on_delete=models.CASCADE)
    time = models.CharField(max_length=4, validators=[validate_24_hour_format], blank=True, null=True)

    def __str__(self):
        return f"Drop at {self.stop_point.name} for {self.bus_route.name} at {self.time}"

class MissingComplaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('found', 'Found'),
        ('not_found', 'Not Found'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_lost = models.DateField()
    image = models.ImageField(upload_to='missing_items/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_reported = models.DateTimeField(auto_now_add=True)

    contact_email = models.EmailField(max_length=254, null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} - {self.status}"


class BusDriver(models.Model):
    name = models.CharField(max_length=255)
    years_of_service = models.PositiveIntegerField()
    cnic_number = models.CharField(max_length=15, unique=True)
    contact_number = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=10)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)  # Average rating out of 5
    image = models.ImageField(upload_to='driver_images/',blank=True,null=True) 

    def __str__(self):
        return self.name

class DriverReview(models.Model):
    driver = models.ForeignKey(BusDriver, related_name='reviews', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating out of 5
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Review by {self.student.username} for {self.driver.name}'
