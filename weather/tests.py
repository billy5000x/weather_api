from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient

class TestWeather(TestCase):

    @patch('requests.get')
    def test_fetch(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "main": {"temp": 20, "humidity": 60}
        }

        client = APIClient()

        response = client.post(
            '/api/weather/fetch-weather/',  
            {"city": "Bogota"},
            format='json'
        )

        self.assertEqual(response.status_code, 201)