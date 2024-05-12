import random
import string
from django import forms 
from django.contrib.auth import get_user_model
from .models import vehicle, Prebook,PaymentReceipt, Feedback, ParkingLot
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class vehicleModelform(forms.ModelForm): 
    class Meta: 
        model = vehicle
        fields = ['Space_to_reserve', 'Full_name', 'entry_time', 'exit_time', 'Vehicle_model', 'vehicle_type', 'vehicle_number','paid']

    def clean(self):
        cleaned_data = super().clean()
        space_to_reserve = cleaned_data.get('Space_to_reserve')
        parking_lot = ParkingLot.objects.last()

        if parking_lot.available_spaces <= 0:
            # If there are no available spaces, raise a validation error
            raise forms.ValidationError("Sorry, there are no available spaces. Please try again later.")
        return cleaned_data
    

class BookingForm(forms.ModelForm):
    class Meta:
        model = Prebook
        labels = {
            'reserved_spaces': 'Space to Reserve:',
            'vehicle_number': 'vehicle_number'
        }
        fields = ['reserved_spaces', 'Full_name', 'entry_time', 'exit_time', 'vehicle_number']

        widgets = {
            'reserved_spaces': forms.NumberInput(attrs={'min': 1}),
            'Full_name': forms.TextInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)   

        # Generate a unique booking ID
        instance.booking_id = self.generate_booking_id()
        
        # Save the multiple vehicle numbers
        vehicle_numbers = self.cleaned_data.get('vehicle_number')
        instance.vehicle_number = vehicle_numbers
        if commit:
            instance.save()
        return instance

    def generate_booking_id(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ['payment_method', 'receipt_image']

class vehicle_form(forms.Form):
    Vehicle_model = forms.CharField()
    license_number = forms.CharField()
    vehicle_type = forms.ChoiceField(choices=[
        ('', "select  "),
        ('2_Wheels', '2 W'),
        ('4_Wheels', '4 W')
    ], required=True)
    
    def clean_vehicle_type(self):
        vehicle_type = self.cleaned_data['vehicle_type']
        if vehicle_type == '':
            raise forms.ValidationError("Please select a valid vehicle type.")
        return vehicle_type

    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "message"]
