from django.contrib import admin
from .models import Update

class UpdateAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'type', 'happening_when', 'link'
    ]

    search_fields = ['title']
    list_filter = ['happening_when']

admin.site.register(Update, UpdateAdmin)