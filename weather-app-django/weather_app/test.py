from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import SearchQuery

class WeatherAppTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.city = 'London'
        
    def test_weather_query_saved_for_authenticated_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='password123')
        
        # Post a search request for weather
        response = self.client.post(reverse('weather'), {'city': self.city})
        
        # Check if the query is saved in the database
        self.assertEqual(SearchQuery.objects.count(), 1)
        query = SearchQuery.objects.first()
        self.assertEqual(query.city, self.city)
        self.assertEqual(query.user, self.user)

    def test_no_queries_for_anonymous_user(self):
        # Simulate an anonymous user accessing the weather page
        response = self.client.get(reverse('weather'))
        
        # Check if the message for unauthenticated users is displayed
        self.assertContains(response, "You must be logged in to see your previous queries.")

    def test_previous_queries_for_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='password123')
        
        # Make a weather query
        self.client.post(reverse('weather'), {'city': self.city})
        
        # Get the response and check if the query appears in previous searches
        response = self.client.get(reverse('weather'))
        self.assertContains(response, self.city)

    def test_no_duplicate_previous_queries_after_multiple_searches(self):
        # Log in the user
        self.client.login(username='testuser', password='password123')
        
        # Make multiple searches for the same city
        self.client.post(reverse('weather'), {'city': self.city})
        self.client.post(reverse('weather'), {'city': self.city})
        
        # Check if only one query is saved
        self.assertEqual(SearchQuery.objects.count(), 1)
        
        # Get the response and check that only one query is shown
        response = self.client.get(reverse('weather'))
        self.assertContains(response, self.city)

    def test_previous_queries_for_unauthenticated_user(self):
        # Simulate an unauthenticated user accessing the weather page
        response = self.client.get(reverse('weather'))
        
        # Check if no previous queries are shown
        self.assertContains(response, "You must be logged in to see your previous queries.")
