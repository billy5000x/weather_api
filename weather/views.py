from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.management import call_command, CommandError
from django.utils.dateparse import parse_date
from .models import WeatherRecord
from .serializers import WeatherRecordSerializer


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = WeatherRecord.objects.all().order_by('-timestamp')
    serializer_class = WeatherRecordSerializer

    
    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        date = self.request.query_params.get('date')

        if city:
            queryset = queryset.filter(city__iexact=city)

        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(timestamp__date=parsed_date)

        return queryset

    
    @action(detail=False, methods=['post'], url_path='fetch-weather')
    def fetch_weather(self, request):
        city = request.data.get('city')

        if not city:
            return Response(
                {"error": "City is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            call_command('fetch_weather', city)

            return Response(
                {"message": f"Weather data for '{city}' fetched successfully"},
                status=status.HTTP_201_CREATED
            )

        except CommandError as e:
            # Error controlado desde el comando (ej: ciudad no encontrada)
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception:
            # Error inesperado
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )