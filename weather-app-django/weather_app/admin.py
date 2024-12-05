from django.contrib import admin
from .models import SearchQuery
from .models import FavoriteLocation

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'date', 'temperature', 'humidity')  # Columns to display in the admin list view
    list_filter = ('city', 'date')  # Filters for sidebar
    search_fields = ('city', 'user__username')  # Search functionality

admin.site.register(FavoriteLocation)