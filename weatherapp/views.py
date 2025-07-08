from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    OPENWEATHER_API_KEY = '666dc6c4b741256bb36eb38355d13257'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=666dc6c4b741256bb36eb38355d13257'
    PARAMS = {'units': 'metric'}

    # Google Custom Search (you need valid keys for this to work)
    GOOGLE_API_KEY = 'AIzaSyCyRdO-Ch5QwBYt_h4FGD-BjYxWtchZWks'  # <-- your Google API key
    SEARCH_ENGINE_ID = '53faddbfcb1de4e74'  # <-- your Search Engine ID
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    search_items = data.get("items")
    if search_items and len(search_items) > 1 and 'link' in search_items[1]:
        image_url = search_items[1]['link']
    else:
        image_url = None  # or a default image URL

    try:
        weather_data = requests.get(url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': ('https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600')
        })
    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred,
            'image_url': image_url
        })