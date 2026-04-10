from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from weather.models import WeatherRecord

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('city', type=str)

    def handle(self, *args, **kwargs):
        city = kwargs['city']
        api_key = settings.API_KEY

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)

        if response.status_code == 404:
            print("Ciudad no encontrada")
            return

        if response.status_code == 401:
            print("API KEY inválida")
            return

        data = response.json()

        WeatherRecord.objects.create(
            city=city,
            temperature=data['main']['temp'],
            humidity=data['main']['humidity']
        )

        print("Datos guardados")