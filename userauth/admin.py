from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):

    list_display = [
        'first_name', 'last_name', 'email',
        'campus', 'matriculation_number'
    ]
    search_fields = [
        'email', 'first_name', 'last_name',
        'mmatriculation_number'
    ]
    list_filter = [
        'user_type', 'faculty', 'department', 'campus',
        'is_staff', 'is_superuser', 'date_joined',
        'last_login'
    ]

admin.site.register(User, UserAdmin)
