from django.urls import path 
from .views import OwnerListView, OwnerCreateView


app_name = 'Owner'

urlpatterns = [
    path('', OwnerListView.as_view(), name='owners-list'),
    path('create/', OwnerCreateView.as_view(), name='owners-create'),

]
