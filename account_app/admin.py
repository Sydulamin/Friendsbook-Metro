from django.contrib import admin
from .models import UserProfile, UserPreference

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'phone_number', 'created_by', 'date_of_birth')
    list_filter = ('gender', 'created_by', 'country', 'religion')
    search_fields = ('name', 'email', 'phone_number', 'country')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'gender', 'date_of_birth', 'email', 'phone_number', 'hide_phone_number')
        }),
        ('Physical Attributes', {
            'fields': ('height', 'weight', 'age'),
        }),
        ('Additional Details', {
            'fields': ('education', 'country', 'address', 'language', 'religion'),
        }),
        ('Meta Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
        }),
    )

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_location', 'preferred_education')
    list_filter = ('preferred_location', 'preferred_education')
    search_fields = ('user__username', 'preferred_location', 'preferred_education')
    ordering = ('user',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Preference Details', {
            'fields': ('user', 'preferred_height_min', 'preferred_height_max', 
                       'preferred_age_min', 'preferred_age_max', 
                       'preferred_weight_min', 'preferred_weight_max', 
                       'preferred_education', 'preferred_location')
        }),
        ('Meta Information', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
