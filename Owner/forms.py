

from django import forms 
from Vehicle.models import Owner

class OwnerModelForm(forms.ModelForm): 
 class Meta:
  model = Owner
  fields = (
   'user', 
  )