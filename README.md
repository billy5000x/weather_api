

Crear entorno virtual:
python3 -m venv venv
source venv/bin/activate
Instalar dependencias:
pip install -r requirements.txt
Crear un archivo .env en la raíz del proyecto:

API_KEY=tu_api_key_de_openweathermap
Migraciones
python manage.py makemigrations
python manage.py migrate
Ejecutar servidor
python manage.py runserver

Acceder a:

http://127.0.0.1:8000/api/weather/
Comando personalizado

Consultar el clima desde terminal:

python manage.py fetch_weather "Bogota"
Endpoints
Obtener registros
GET /api/weather/

Filtrar por ciudad:

GET /api/weather/?city=Bogota

Filtrar por fecha:

GET /api/weather/?date=2026-04-10
Obtener clima desde API externa
POST /api/weather/fetch-weather/

Body:

{
  "city": "Bogota"
}

Respuesta:

{
  "message": "Weather data for 'Bogota' fetched successfully"
}

Testing

Ejecutar pruebas:
python manage.py test

Tecnologías utilizadas
Django 6.0.4
Django REST Framework 3.17.1
SQLite
Requests
Python Dotenv