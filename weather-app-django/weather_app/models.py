# weather_app/models.py

from django.db import models
from django.contrib.auth.models import User

class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="search_queries")  
    city = models.CharField(max_length=255)  
    date = models.DateTimeField(auto_now_add=True) 
    temperature = models.FloatField(null=True, blank=True)  
    humidity = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return f"Query: {self.city} by {self.user.username if self.user else 'Anonymous'} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

# weather_app/models.py

class FavoriteLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_locations")
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.city
