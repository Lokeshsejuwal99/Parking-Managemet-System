from django import views
from django.urls import path
from .views import (
    ParkingLotInfoView,
    PrebookView,
    VehicleListview,
    Faqview,
    VehicleCreateview,
    AboutView,
    submit_feedback,
    admin_feedback,
    Contactview,
)
from Vehicle.views import *

app_name = "Vehicle"


urlpatterns = [
    path("", VehicleListview.as_view(), name="vehicle-list"),
    path("<int:pk>/update/", VehicleUpdateView.as_view(), name="vehicle-update"),
    path("<int:pk>/delete/", VehicleDeleteView.as_view(), name="vehicle-delete"),
    path(
        "prebook/<int:pk>/update/", PrebookUpdateView.as_view(), name="prebook-update"
    ),
    path(
        "prebook/<int:pk>/delete/", PrebookDeleteView.as_view(), name="prebook-delete"
    ),
    path("parking_lot/", ParkingLotInfoView.as_view(), name="parking_lot_info"),
    path("prebook/<int:prebook_id>/pay/", payment_view, name="payment_view"),
    path("vehicle/create/", VehicleCreateview.as_view(), name="vehicle-create"),
    path("vehicle/dashboard/", DashboardView, name="vehicle-dashboard"),
    path("bookconfig/", BookedDetailView.as_view(), name="bookconfig"),
    path("vehicle/unpaid/", UnpaidVehiclesView, name="vehicle-unpaid"),
    path("vehicle/paid/", PaidVehiclesView, name="vehicle-paid"),
    path("prebook/", PrebookView.as_view(), name="prebook"),
    path("prebookedlist/", PrebookedlistView, name="prebookedlist"),
    path("useronly/", Olny_user, name="onlyuser"),
    path("success/", success_view, name="success_view"),
    path("feedback/", submit_feedback, name="feedback"),
    path("admin_feedback/", admin_feedback, name="admin_feedback"),
    path("space_full/", SpacefullView, name="space-full"),
    path("about/", AboutView, name="about"),
    path("FAQ/", Faqview, name="FAQ"),
    path("contact/", Contactview, name="contact"),
    path("generate_invoice/<int:pk>/", GeneratePdf.as_view(), name="generate_invoice"),
    # khalti urls
    path("initiate", initkhalti, name="initiate"),
    path("verify", verifykhalti, name="verify"),
]
