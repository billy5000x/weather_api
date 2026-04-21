from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.management import call_command, CommandError
from django.utils.dateparse import parse_date
from .models import WeatherRecord
from .serializers import WeatherRecordSerializer
from datetime import datetime
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = WeatherRecord.objects.filter(is_deleted=False).order_by('-timestamp')
    serializer_class = WeatherRecordSerializer
    @action(detail=False, methods=['get'], url_path='latest')
    def latest(self, request):
            limit = int(request.query_params.get('limit', 5))

            queryset = WeatherRecord.objects.filter(is_deleted=False).order_by('-timestamp')[:limit]

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # obtiene el registro

        instance.is_deleted = True   # 👈 lo marca como eliminado
        instance.save()              # guarda el cambio

        return Response(
        {"message": "Registro eliminado correctamente"},
        status=200
    )
    def get_queryset(self):
        queryset = WeatherRecord.objects.filter(is_deleted=False).order_by('-timestamp')

        city = self.request.query_params.get('city')
        date = self.request.query_params.get('date')

        if city:
            queryset = queryset.filter(city__iexact=city)

        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                start = timezone.make_aware(datetime.combine(parsed_date, datetime.min.time()))
                end = timezone.make_aware(datetime.combine(parsed_date, datetime.max.time()))
                queryset = queryset.filter(timestamp__range=(start, end))

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
            
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception:
           
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        