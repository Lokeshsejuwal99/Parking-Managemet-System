from django.core.management.base import BaseCommand
from Vehicle.models import ParkingLot
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Create ParkingLot instances for each day of the week'

    def handle(self, *args, **options):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())

        for day_offset in range(7):
            current_date = start_of_week + timedelta(days=day_offset)
            
            # Check if a ParkingLot instance already exists for the current date
            if not ParkingLot.objects.filter(date=current_date).exists():
                ParkingLot.objects.create(date=current_date, name=f'Parking Lot {current_date}', total_spaces=500, available_spaces=500)
                self.stdout.write(self.style.SUCCESS(f'Successfully created ParkingLot instance for {current_date}'))
            else:
                self.stdout.write(self.style.WARNING(f'ParkingLot instance for {current_date} already exists'))
