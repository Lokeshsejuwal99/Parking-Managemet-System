# Vehicle/utils.py
import string
import random

from .models import Prebook, vehicle, models


def generate_booking_id(length=8):
    while True:
        booking_id = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )
        if not Prebook.objects.filter(booking_id=booking_id).exists():
            print(f"Generated Booking ID: {booking_id}")
            return booking_id

        booking_id = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )
        if not vehicle.objects.filter(booking_id=booking_id).exists():
            print(f"Generated Booking ID: {booking_id}")
            return booking_id


def calculate_total_amount():
    # Retrieve total_amount from Vehicle model
    vehicle_total_amount = (
        vehicle.objects.aggregate(total_amount=models.Sum("total_amount"))[
            "total_amount"
        ]
        or 0
    )

    # Retrieve total_amount from Prebook model
    prebook_total_amount = (
        Prebook.objects.aggregate(total_amount=models.Sum("total_amount"))[
            "total_amount"
        ]
        or 0
    )

    # Calculate the total amount
    total_amount = vehicle_total_amount + prebook_total_amount

    return total_amount
