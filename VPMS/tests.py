from django.test import TestCase
from .models import vehicle, Prebook, ParkingLot, BillNumber
from django.utils import timezone
from datetime import datetime


class ModelTestCase(TestCase):
    def setUp(self):
        self.parking_lot = ParkingLot.objects.create(
            name="Test Parking Lot", total_spaces=100
        )
        self.vehicle = vehicle.objects.create(
            parking_lot=self.parking_lot,
            Full_name="Test User",
            entry_time=timezone.now(),
        )

    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.Full_name, "Test User")
        self.assertTrue(self.vehicle.booking_id)
        self.assertFalse(self.vehicle.paid)

    def test_prebook_creation(self):
        prebook = Prebook.objects.create(
            parking_lot=self.parking_lot,
            Full_name="Test User",
            entry_time=timezone.now(),
        )
        self.assertEqual(prebook.Full_name, "Test User")
        self.assertTrue(prebook.booking_id)

    def test_parking_lot_creation(self):
        self.assertEqual(self.parking_lot.name, "Test Parking Lot")
        self.assertEqual(self.parking_lot.available_spaces, 100)
        self.assertEqual(self.parking_lot.total_reserved_spaces, 0)

    def test_bill_number_creation(self):
        bill_number = BillNumber.objects.create(bill_no=1)
        self.assertEqual(bill_number.bill_no, 1)

    def test_vehicle_space_reservation(self):
        reserved_spaces = self.vehicle.Space_to_reserve
        self.assertEqual(
            self.vehicle.parking_lot.available_spaces, 100 - reserved_spaces
        )
        self.assertEqual(
            self.vehicle.parking_lot.total_reserved_spaces, reserved_spaces
        )

    def test_prebook_space_reservation(self):
        prebook = Prebook.objects.create(
            parking_lot=self.parking_lot,
            Full_name="Test User",
            entry_time=timezone.now(),
            reserved_spaces=2,
        )
        reserved_spaces = prebook.reserved_spaces
        self.assertEqual(prebook.parking_lot.available_spaces, 100 - reserved_spaces)
        self.assertEqual(prebook.parking_lot.total_reserved_spaces, reserved_spaces)

    def test_vehicle_delete(self):
        initial_available_spaces = self.parking_lot.available_spaces
        self.vehicle.delete()
        self.assertEqual(
            self.parking_lot.available_spaces,
            initial_available_spaces + self.vehicle.Space_to_reserve,
        )

    def test_prebook_delete(self):
        initial_available_spaces = self.parking_lot.available_spaces
        prebook = Prebook.objects.create(
            parking_lot=self.parking_lot,
            Full_name="Test User",
            entry_time=timezone.now(),
            reserved_spaces=2,
        )
        prebook.delete()
        self.assertEqual(
            self.parking_lot.available_spaces,
            initial_available_spaces + prebook.reserved_spaces,
        )
