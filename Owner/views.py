from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, reverse
from django.views import generic
from .forms import OwnerModelForm
from Vehicle.models import Owner
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class OwnerListView(LoginRequiredMixin, generic.ListView):
    template_name = "Owner/owners.html"

    def get_queryset(self):
        return Owner.objects.all()


class OwnerCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "Owner/owners_create.html"
    form_class = OwnerModelForm

    def get_success_url(self):
        return reverse("Owner:owners-list")

    def form_valid(self, form):
        owner = form.save(commit=False)
        owner.organization = self.request.user.userprofile
        owner.save()
        return super(OwnerCreateView, self).form_valid(form)
