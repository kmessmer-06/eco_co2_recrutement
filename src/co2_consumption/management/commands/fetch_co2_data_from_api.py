from django.core.management.base import BaseCommand
from src.co2_consumption.serializers import ConsumptionSerializer
import requests


class Command(BaseCommand):
    help = 'Fetch data from ECO CO2 API'

    def handle(self, *args, **options):
        response = requests.get(
            'http://api-recrutement.ecoco2.com/v1/data/?start=1483225200&end=1546297200'
        )
        data = response.json()

        serializer = ConsumptionSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()


        print("CONSUMPTION OBJECTS CREATED : {}".format(len(data)))
