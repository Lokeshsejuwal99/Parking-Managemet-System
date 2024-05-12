import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta 
from django.utils import timezone
from django.db.models.signals import post_delete    
from django.dispatch import receiver
from django.db.models import Sum
from django.shortcuts import redirect, render
from django import forms
# Create your models here.
class User(AbstractUser):
    pass

class UserProfile(models.Model): 
   user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

   def __str__(self):
    return self.user.username
   
class ParkingLot(models.Model):
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=30, null=False, default=None)
    total_spaces = models.PositiveIntegerField(default=500)
    available_spaces = models.PositiveIntegerField(default=500)
    total_reserved_spaces = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

def default_exit_time():
    return datetime.now()+timedelta(hours=1)

class vehicle(models.Model):    
  parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
  Space_to_reserve = models.PositiveIntegerField(default=1)
  Full_name = models.CharField(max_length=30, null=False, default=None)
  entry_time = models.DateTimeField(default=datetime.now)
  exit_time = models.DateTimeField(null=False, blank=False, default=default_exit_time)
  Vehicle_model = models.CharField(max_length=30,blank=True, null=True)
  vehicle_type = models.CharField(max_length=10, choices=[('2_Wheels','2 W'),('4_Wheels', '4 W')])
  total_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
  booking_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
  vehicle_number = models.CharField(max_length=255, unique=False, blank=True, null=True)
  paid = models.BooleanField(default=False)
  
  def __str__(self):
     return f"{self.Full_name} - {self.booking_id}"
  def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)
    self._original_Space_to_reserve = self.Space_to_reserve

  def save(self, *args, **kwargs):
    if self.parking_lot.available_spaces < self.Space_to_reserve:
        return redirect('Vehicle/space_full.html')
    
    if not self.booking_id:
        self.booking_id = self.generate_booking_id()

    is_new_instance = self.pk is None
    if is_new_instance or self.Space_to_reserve != self._original_Space_to_reserve:
        if self.Space_to_reserve <= self.parking_lot.available_spaces:
            if not is_new_instance:
                self.parking_lot.available_spaces += self._original_Space_to_reserve
                self.parking_lot.total_reserved_spaces -= self._original_Space_to_reserve
            self.parking_lot.available_spaces -= self.Space_to_reserve
            self.parking_lot.total_reserved_spaces += self.Space_to_reserve
            self.parking_lot.save()

        # Ensure that exit_time is set
    if self.exit_time is not None:
        self.total_amount = self.calculate_parking_fee()
        super().save(*args, **kwargs)
        print("Saving Prebook instance...")
    else:
        self.error_message = "No space available, Please try again later"
        super().save(*args, **kwargs)

  def generate_booking_id(self, length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
  
  def multiple_vehicles(self, total_fee, Space_to_reserve):
    if int(Space_to_reserve) > 1:
        total = total_fee * Space_to_reserve
        return total
    else:
        return total_fee
    
  def calculate_parking_fee(self):
      if self.exit_time is not None:
          parked_hours = (self.exit_time - self.entry_time).total_seconds() / 3600
          base_fee = 50
          additional_fee_per_hour = 40  
          if parked_hours <= 1:
              return base_fee * self.Space_to_reserve
          else:
              total_fee = base_fee + additional_fee_per_hour * (parked_hours - 1)
              return self.multiple_vehicles(total_fee, self.Space_to_reserve)
      else:
          return base_fee


@receiver(post_delete, sender=vehicle)
def update_available_spaces_on_vehicle_delete(sender, instance, **kwargs):
    instance.parking_lot.available_spaces += instance.Space_to_reserve
    instance.parking_lot.total_reserved_spaces -= instance.Space_to_reserve
    instance.parking_lot.save()


class Prebook(models.Model):
    Full_name = models.CharField(max_length=30, null=False, default=None)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    reserved_spaces = models.PositiveIntegerField(default=1)
    entry_time = models.DateTimeField(default=datetime.now)
    exit_time = models.DateTimeField(default=default_exit_time, blank=False)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    booking_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
    vehicle_number = models.CharField(max_length=255, unique=False, blank=True, null=True)
    
    def __str__(self):
        return f'{self.Full_name} - {self.vehicle_number}'
      
    def save(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_Space_to_reserve = self.reserved_spaces

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()

        is_new_instance = self.pk is None
        if is_new_instance or self.reserved_spaces != self._original_Space_to_reserve:
            if self.reserved_spaces <= self.parking_lot.available_spaces:
                if not is_new_instance:
                    self.parking_lot.available_spaces += self._original_Space_to_reserve
                    self.parking_lot.total_reserved_spaces -= self._original_Space_to_reserve
                self.parking_lot.available_spaces -= self.reserved_spaces
                self.parking_lot.total_reserved_spaces += self.reserved_spaces
                self.parking_lot.save()


            # Ensure that exit_time is set
            if self.exit_time is not None:
                self.total_amount = self.calculate_parking_fee()
            super().save(*args, **kwargs)
            print("Saving Prebook instance...")
        else:
            self.error_message = "No space available, Please try again later"
            super().save(*args, **kwargs)

    def generate_booking_id(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def multiple_vehicles(self, total_fee, reserved_spaces):
        if reserved_spaces > 1:
            total = total_fee * reserved_spaces
            return total
        else:
            return total_fee

    def calculate_parking_fee(self):
        if self.exit_time is not None:
            parked_hours = (self.exit_time - self.entry_time).total_seconds() / 3600
            base_fee = 50
            additional_fee_per_hour = 40

            if parked_hours <= 1:
                total_fee = base_fee
            else:
                total_fee = base_fee + additional_fee_per_hour * (parked_hours - 1)
            return self.multiple_vehicles(total_fee, self.reserved_spaces)
        else:
            return None


@receiver(post_delete, sender=Prebook)
def update_available_spaces_on_vehicle_delete(sender, instance, **kwargs):
    instance.parking_lot.available_spaces += instance.reserved_spaces
    instance.parking_lot.total_reserved_spaces -= instance.reserved_spaces
    instance.parking_lot.save()

class PaymentReceipt(models.Model):
    prebook = models.ForeignKey(Prebook, on_delete=models.CASCADE)
    receipt_image = models.ImageField(upload_to='receipt_image/', default=None)
    payment_method = models.CharField(max_length=10, choices=[('E-sewa','E-sewa'),('Khalti', 'Khalti'), ('Bank','Bank')], default=None)

    def __str__(self):
        return f"Receipt for Prebook ID {self.prebook_id}"
    
class Owner(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
   def __str__(self):
    return self.user.username
      

class Feedback(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=30, null=False, blank=False) 
    message = models.TextField(max_length=300, null=False)
   
def calculate_total_amount():
    # Retrieve total_amount from Vehicle model
    vehicle_total_amount = vehicle.objects.aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0
    
    # Retrieve total_amount from Prebook model
    prebook_total_amount = Prebook.objects.aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0
    
    # Calculate the total amount
    total_amount = vehicle_total_amount + prebook_total_amount
    
    return total_amount

class BillNumber(models.Model):
    bill_no = models.IntegerField(unique=True)