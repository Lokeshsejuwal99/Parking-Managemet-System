from django.contrib import admin
from .models import User, vehicle, ParkingLot, Prebook, UserProfile, Owner, PaymentReceipt

# Register your models here.
admin.site.register(User)
admin.site.register(vehicle)
admin.site.register(ParkingLot)
admin.site.register(Prebook)
admin.site.register(PaymentReceipt)
admin.site.register(Owner)
admin.site.register(UserProfile)