from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'happening_when', 'event_type',
        'tag', 'level', 'created_when'
    ]

    search_fields = [
        'title', 
    ]

    list_filter = [
        'event_type', 'tag', 'level', 'happening_when'
    ]

admin.site.register(Event, EventAdmin)