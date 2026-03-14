from django.contrib import admin
from .models import Update


class UpdateAdmin(admin.ModelAdmin):

    list_display = [
        'title', 'type', 'tag', 'happening_when', 'link'
    ]

    search_fields = ['title']
    list_filter = ['type', 'tag', 'happening_when']


admin.site.register(Update, UpdateAdmin)