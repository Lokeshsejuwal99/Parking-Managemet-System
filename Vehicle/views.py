from .models import vehicle
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from Vehicle.models import ParkingLot, vehicle, Prebook
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout as logouts
from django.contrib.auth.mixins import LoginRequiredMixin
from Vehicle.utils import calculate_total_amount
from .forms import (
    vehicleModelform,
    CustomUserCreationForm,
    BookingForm,
    PaymentForm,
    FeedbackForm,
)
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.http import HttpResponse
import random
import json
from django.template.loader import get_template
import string
from io import BytesIO



User = get_user_model()


def superuser_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)

            return redirect("Vehicle:vehicle-list")
        else:
            messages.error(request, "Invalid username or password.")
    return render(
        request,
        "Vehicle/only_users.html",
        {"error_message": "Invalid username or password."},
    )


def homepage(request):
    return render(request, "Vehicle/homepage.html")


def Contactview(request):
    return render(request, "Vehicle/contact.html")


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def admin_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, "Vehicle/admin_feedback.html", {"feedbacks": feedbacks})


def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FeedbackForm()
    return render(request, "Vehicle/feedback.html", {"form": form})


def Faqview(request):
    return render(request, "Vehicle/FAQ.html")


def AboutView(request):
    return render(request, "Vehicle/about.html")


def DashboardView(request):
    today = timezone.now().date()

    # Calculate the start and end dates for the week
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Filter DailyData for the current week
    weekly_data = ParkingLot.objects.filter(date__range=[start_of_week, end_of_week])

    # Query ParkingLot data
    parking_lots = ParkingLot.objects.all()

    # Query total amount
    total_amount = calculate_total_amount()

    # Process the data as needed
    labels = []
    available_spaces_data = []
    total_reserved_data = []

    # Populate the lists with data for each day of the week
    for day in range(7):
        date = start_of_week + timedelta(days=day)
        daily_data = weekly_data.filter(date=date).first()

        if daily_data:
            labels.append(date.strftime("%Y-%m-%d"))
            available_spaces_data.append(daily_data.available_spaces)
            total_reserved_data.append(daily_data.total_reserved_spaces)
        else:
            labels.append(date.strftime("%Y-%m-%d"))
            available_spaces_data.append(500)
            total_reserved_data.append(0)

    morning_start = time(6, 0, 0)
    afternoon_start = time(12, 0, 0)
    evening_start = time(18, 0, 0)

    # Filter vehicles based on entry time
    morning_vehicles = vehicle.objects.filter(entry_time__time__lt=afternoon_start)
    afternoon_vehicles = vehicle.objects.filter(
        entry_time__time__lt=evening_start
    ).exclude(entry_time__time__lt=morning_start)
    evening_vehicles = vehicle.objects.filter(entry_time__time__gte=evening_start)

    # Filter prebooked spaces based on entry time
    morning_prebooked = Prebook.objects.filter(entry_time__time__lt=afternoon_start)
    afternoon_prebooked = Prebook.objects.filter(
        entry_time__time__lt=evening_start
    ).exclude(entry_time__time__lt=morning_start)
    evening_prebooked = Prebook.objects.filter(entry_time__time__gte=evening_start)

    # Aggregate data based on total spaces reserved
    morning_count = (
        morning_vehicles.aggregate(Sum("Space_to_reserve"))["Space_to_reserve__sum"]
        or 0
    )
    afternoon_count = (
        afternoon_vehicles.aggregate(Sum("Space_to_reserve"))["Space_to_reserve__sum"]
        or 0
    )
    evening_count = (
        evening_vehicles.aggregate(Sum("Space_to_reserve"))["Space_to_reserve__sum"]
        or 0
    )

    # Aggregate prebooked spaces
    morning_prebooked_count = (
        morning_prebooked.aggregate(Sum("reserved_spaces"))["reserved_spaces__sum"] or 0
    )
    afternoon_prebooked_count = (
        afternoon_prebooked.aggregate(Sum("reserved_spaces"))["reserved_spaces__sum"]
        or 0
    )
    evening_prebooked_count = (
        evening_prebooked.aggregate(Sum("reserved_spaces"))["reserved_spaces__sum"] or 0
    )

    # Add prebooked spaces to the counts for vehicles
    morning_count += morning_prebooked_count
    afternoon_count += afternoon_prebooked_count
    evening_count += evening_prebooked_count

    context = {
        "labels": labels,
        "available_spaces_data": available_spaces_data,
        "total_reserved_data": total_reserved_data,
        "parking_lots": parking_lots,
        "total_amount": total_amount,
        "morning_count": morning_count or 0,
        "afternoon_count": afternoon_count or 0,
        "evening_count": evening_count or 0,
    }

    return render(request, "Vehicle/dashboard.html", context)


def Olny_user(request):
    return render(request, "Vehicle/only_users.html")


def SpacefullView(request):
    return render(request, "Vehicle/space_full.html")


def UnpaidVehiclesView(request):
    vehicles = vehicle.objects.filter(paid=False)
    return render(request, "Vehicle/unpaid_vehicles.html", {"vehicles": vehicles})


def PaidVehiclesView(request):
    vehicles = vehicle.objects.filter(paid=True)
    return render(request, "Vehicle/paid_vehicles.html", {"vehicles": vehicles})


def PrebookedlistView(request):
    prebook = Prebook.objects.all()
    return render(request, "Vehicle/prebookedlist.html", {"prebook": prebook})


class VehicleSignupview(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        send_welcome_email(self.object.email)
        return response


def send_welcome_email(user_email):
    print(f"Sending welcome email to: {user_email}")
    subject = "Welcome to Vehicle-parking Management System!"
    message = "Thank you for registering. We are excited to have you!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


class LandingView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class VehicleListview(LoginRequiredMixin, generic.ListView):
    template_name = "Vehicle/vehicle_list.html"
    queryset = vehicle.objects.all()
    context_object_name = "Vehicle"

    def get_success_url(self):
        return reverse("landing.html")


def vehicle_list(request):
    Vehicle = vehicle.objects.all()
    context = {"Vehicle": Vehicle}
    return render(request, "Vehicle/vehicle_list.html", context)


class VehicleCreateview(generic.CreateView):
    template_name = "Vehicle/vehicle_create.html"
    form_class = vehicleModelform
    model = vehicle
    success_url = reverse_lazy("Vehicle:vehicle-create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parking_lot"] = ParkingLot.objects.first()
        return context

    def form_valid(self, form):
        parking_lot = ParkingLot.objects.first()
        space_to_reserve = form.cleaned_data.get("Space_to_reserve")

        if parking_lot.available_spaces <= space_to_reserve:
            # If there are not enough available spaces, redirect to the
            # space-full.html page
            return redirect("Vehicle:space-full")

        # If there are available spaces, proceed with form validation
        form.instance.parking_lot = parking_lot
        form.instance.User = self.request.user
        form.instance.booking_id = generate_booking_id()

        # Allow multiple vehicle numbers
        form.instance.vehicle_number = form.cleaned_data["vehicle_number"]
        # Set success message
        messages.success(self.request, "Vehicle has been added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = vehicle
    template_name = "Vehicle/vehicle_update.html"
    form_class = vehicleModelform
    context_object_name = "vehicle"
    success_url = reverse_lazy("Vehicle:vehicle-unpaid")

    def message_alert(request):
        messages.success(request, "Vehicle has been updated successfully.")
        return redirect(request, "Vehicle:vehicle-unpaid")

    def get_success_url(self):

        if self.object.paid:
            return reverse_lazy("Vehicle:vehicle-paid")
        else:
            return reverse_lazy("Vehicle:vehicle-unpaid")


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = vehicle
    template_name = "Vehicle/vehicle_delete.html"
    success_url = reverse_lazy("Vehicle:vehicle-unpaid")

    def get_success_url(self):
        if self.object.paid:
            return reverse_lazy("Vehicle:vehicle-paid")
        else:
            return reverse_lazy("Vehicle:vehicle-unpaid")


class PrebookView(LoginRequiredMixin, generic.CreateView):
    template_name = "Vehicle/prebook.html"
    form_class = BookingForm
    model = Prebook

    def get_success_url(self):
        return reverse("Vehicle:bookconfig")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parking_lot"] = ParkingLot.objects.first()
        return context

    def form_valid(self, form):
        parking_lot = ParkingLot.objects.first()
        form.instance.parking_lot = parking_lot
        form.instance.User = self.request.user
        form.instance.booking_id = generate_booking_id()

        # Allow multiple vehicle numbers
        form.instance.vehicle_numbers = form.cleaned_data["vehicle_number"]
        return super().form_valid(form)


class PrebookUpdateView(LoginRequiredMixin, UpdateView):
    model = Prebook
    template_name = "Vehicle/prebook_update.html"
    form_class = BookingForm
    context_object_name = "prebook"
    success_url = reverse_lazy("Vehicle:prebookedlist")


class PrebookDeleteView(LoginRequiredMixin, DeleteView):
    model = Prebook
    template_name = "Vehicle/prebook_delete.html"
    success_url = reverse_lazy("Vehicle:prebookedlist")


class ParkingLotInfoView(generic.DetailView):
    template_name = "Vehicle/parking_lot_info.html"

    def get(self, request, *args, **kwargs):
        parking_lot = ParkingLot.objects.first()
        return render(request, self.template_name, {"parking_lot": parking_lot})


class BookedDetailView(DetailView):
    model = Prebook
    template_name = "Vehicle/bookconfig.html"
    context_object_name = "prebook"

    def get_object(self):
        # Retrieve the most recent booking
        return Prebook.objects.order_by("-id").first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if there is a booking
        if self.object:
            context["booking_id"] = self.object.booking_id
            context["vehicle_numbers"] = self.object.vehicle_number.split(",")
            context["full_name"] = self.object.Full_name
            context["entry_time"] = self.object.entry_time
            context["exit_time"] = self.object.exit_time
            context["total_amount"] = self.object.calculate_parking_fee()
        else:
            context["booking_id"] = None
            context["vehicle_numbers"] = []
            context["full_name"] = None
            context["entry_time"] = None
            context["exit_time"] = None
            context["total_amount"] = None

        return context


def payment_view(request, prebook_id):
    prebook_instance = Prebook.objects.get(pk=prebook_id)
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment_instance = form.save(commit=False)
            payment_instance.prebook = prebook_instance
            payment_instance.save()
            return redirect("Vehicle:success_view")
        else:
            print(form.errors)
    else:
        form = PaymentForm()
    return render(
        request, "payment.html", {"form": form, "prebook_id": prebook_instance.id}
    )


def success_view(request):
    return render(request, "payment_success.html")


def generate_booking_id(length=8):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def logout(request):
    if request.method == "POST":
        logouts(request)
        return redirect("landing-page")


def totalamount_view(request):
    total_amount = calculate_total_amount()
    return render(request, "Vehicle/dashboard.html", {"total_amount": total_amount})


def reserve_vehicle(request):
    if request.method == "POST":
        form = vehicleModelform(request.POST)
        if form.is_valid():
            # Extract entry date from the form data
            entry_date = form.cleaned_data["entry_time"].date()

            # Retrieve or create ParkingLot instance for the entry date
            parking_lot, _ = ParkingLot.objects.get_or_create(date=entry_date)

            # Update available_spaces and total_reserved_spaces
            reserved_spaces = form.cleaned_data["Space_to_reserve"]
            parking_lot.available_spaces -= reserved_spaces
            parking_lot.total_reserved_spaces += reserved_spaces

            # Save the ParkingLot instance
            parking_lot.save()

            # Save the form instance
            form.save()

            # Redirect to success page or any other page
            return redirect("success_page_url")

    else:
        form = vehicleModelform()

    return render(request, "Vehicle/vehicle_create.html", {"form": form})


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


class GeneratePdf(ListView):
    def get(self, request, pk, *args, **kwargs):
        date = datetime.now()
        first_bill_number = BillNumber.objects.first()
        if first_bill_number:
            bill_no = first_bill_number.bill_no
        else:
            bill_no = 1
        # Increment the bill number for the next bill
        next_bill_number = bill_no + 1
        BillNumber.objects.update_or_create(defaults={"bill_no": next_bill_number})
        prebook = Prebook.objects.filter(id=pk).values(
            "booking_id",
            "Full_name",
            "reserved_spaces",
            "vehicle_number",
            "entry_time",
            "exit_time",
            "total_amount",
        )
        Vehicle = vehicle.objects.filter(id=pk).values(
            "booking_id",
            "Full_name",
            "Space_to_reserve",
            "vehicle_number",
            "Vehicle_model",
            "entry_time",
            "exit_time",
            "total_amount",
        )

        context = {
            "data": {
                "bill_no": bill_no,
                "date": date,
                "location": "NewRoad-24, Kathmandu, Nepal",
                "email": "vpmsnepal3232@gmail.com",
            },
            "prebook": prebook,
            "vehicle": Vehicle,
        }
        pdf = render_to_pdf("Vehicle/generate_invoice.html", context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = f"Invoice"
            content = f"inline; filename='{filename}'"
            download = request.GET.get("download")
            if download:
                content = f"attachment; filename='{filename}'"
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Not found")


def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get("landing-page")
    purchase_order_id = request.POST.get("purchase_order_id")
    amount = request.POST.get("amount")

    print("return_url", return_url)
    print("purchase_order_id", purchase_order_id)
    print("amount", amount)

    payload = json.dumps(
        {
            "return_url": "http://127.0.0.1:8000/",
            "website_url": "https://127.0.0.1:8000/",
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": "lokesh",
                "email": "lokesh@gmail.com",
                "phone": "9865367362",
            },
        }
    )
    headers = {
        "Authorization": "key test_secret_key_045465976732450987e599caa9680fcc",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res["payment_url"])


def verifykhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    pidx = request.GET.get("pidx")
    headers = {
        "Authorization": "key test_secret_key_045465976732450987e599caa9680fcc",
        "Content-Type": "application/json",
    }

    payload = json.dumps(
        {
            "pidx": pidx,
        }
    )

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    new_res = json.loads(response.text)
    print(new_res)


def pay_vehicle(request, vehicle_id):
    # Retrieve the vehicle instance
    vehicle_instance = get_object_or_404(vehicle, id=vehicle_id)

    # Set the paid status to True
    vehicle_instance.paid = True
    vehicle_instance.save()

    # Redirect to a success page or any other page
    return redirect("Vehicle:vehicle-paid")
