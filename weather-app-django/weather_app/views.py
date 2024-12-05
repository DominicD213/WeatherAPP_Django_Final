from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SearchQuery, FavoriteLocation
from .forms import FavoriteLocationForm
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = str(os.getenv('WEATHER_API_KEY'))

def get_weather_data(city, weather_api_key):
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    current_weather_res = requests.get(current_weather_url.format(city, weather_api_key)).json()

    print("API Response:", current_weather_res)  # Add this for debugging

    if current_weather_res.get('cod') != 200:
        raise ValueError(f"Error fetching data: {current_weather_res.get('message', 'Unknown error')}")

    current_weather_data = {
        'date': datetime.datetime.fromtimestamp(current_weather_res['dt']).strftime('%a, %b %d'),
        'city': city,
        'temperature': current_weather_res['main']['temp'],
        'min_temp': current_weather_res['main']['temp_min'],
        'max_temp': current_weather_res['main']['temp_max'],
        'humidity': current_weather_res['main']['humidity'],
        'description': current_weather_res['weather'][0]['description'],
        'icon': current_weather_res['weather'][0]['icon'],
    }

    return current_weather_data


def weather_view(request):
    if request.method == 'POST':
        city = request.POST['city']
        current_weather = get_weather_data(city, WEATHER_API_KEY)

        if request.user.is_authenticated:
            existing_query = SearchQuery.objects.filter(user=request.user, city=city).first()
            if not existing_query:
                SearchQuery.objects.create(
                    user=request.user,
                    city=city,
                    temperature=current_weather['temperature'],
                    humidity=current_weather['humidity'],
                )

        # Retrieve unique queries from the database for the authenticated user
        if request.user.is_authenticated:
            previous_queries = SearchQuery.objects.filter(user=request.user).order_by('-date')
            seen_cities = set()
            unique_queries = []
            for query in previous_queries:
                if query.city not in seen_cities:
                    unique_queries.append(query)
                    seen_cities.add(query.city)
        else:
            unique_queries = []  # No queries for unauthenticated users

        # Fetch the favorites for the authenticated user
        if request.user.is_authenticated:
            favorites = FavoriteLocation.objects.filter(user=request.user)
        else:
            favorites = []  # Empty list if the user is not authenticated

        return render(request, 'weather.html', {
            'current_weather': current_weather,
            'previous_queries': unique_queries,
            'favorites': favorites,  # Add favorites to the context
        })
    else:
        # Get unique search queries for authenticated users, otherwise an empty list
        if request.user.is_authenticated:
            previous_queries = SearchQuery.objects.filter(user=request.user).order_by('-date')
            seen_cities = set()
            unique_queries = []
            for query in previous_queries:
                if query.city not in seen_cities:
                    unique_queries.append(query)
                    seen_cities.add(query.city)
        else:
            unique_queries = []  # No queries for unauthenticated users

        # Fetch the favorites for the authenticated user
        if request.user.is_authenticated:
            favorites = FavoriteLocation.objects.filter(user=request.user)
        else:
            favorites = []  # Empty list if the user is not authenticated

        return render(request, 'weather.html', {
            'previous_queries': unique_queries,
            'favorites': favorites,  # Add favorites to the context
        })


def favorite_locations(request):
    if request.user.is_authenticated:
        favorites = FavoriteLocation.objects.filter(user=request.user)
    else:
        favorites = []  # Empty list for unauthenticated users
    return render(request, 'favorites/favorites.html', {'favorites': favorites})


def add_favorite_location(request):
    if request.method == 'POST':
        form = FavoriteLocationForm(request.POST)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.save()
            return redirect('weather')
    else:
        form = FavoriteLocationForm()
    return render(request, 'favorites/add_favorite.html', {'form': form})


def remove_favorite_location(request, pk):
    if request.user.is_authenticated:
        favorite = get_object_or_404(FavoriteLocation, pk=pk, user=request.user)
        favorite.delete()
        return redirect('favorite_locations')
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated
