import requests

API_KEY = 'd76b098ca73896678f72adb83261f5c2'
URL = 'https://api.openweathermap.org/data/2.5/weather'

params = {
    # 'q': 'Kyiv',
    "lat": 33.44,
    "lon": -94.04,
    'appid': API_KEY,
    'units': 'metric'}

response = requests.get(url=URL, params=params)

print(response.url)

print(response.status_code)

print(response.text)
