from django.core.management.base import BaseCommand
from src.co2_consumption.models import Consumption, ConsumptionInterpolate


class Command(BaseCommand):
    help = 'Generate consumption by hours data'

    def handle(self, *args, **options):
        qs = Consumption.objects.filter(datetime__minute=0, datetime__second=0)
        counter = 0

        for consumption in qs.iterator():
            _, created = ConsumptionInterpolate.objects.get_or_create(
                co2_rate=consumption.co2_rate,
                datetime=consumption.datetime
            )

            counter = counter+1 if created else counter

        print("CONSUMPTIONINTERPOLATE OBJECTS CREATED : {}".format(counter))
