from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, UserPreference

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'gender', 'phone_number', 'created_by', 'date_of_birth', 'profile_picture_preview')
    list_filter = ('gender', 'created_by', 'country', 'religion')
    search_fields = ('name', 'email', 'phone_number', 'country')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'profile_picture', 'name', 'gender', 'date_of_birth', 'email', 'phone_number', 'hide_phone_number')
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

    def profile_picture_preview(self, obj):
        """Displays the user's profile picture as a thumbnail in the admin panel."""
        if obj.profile_pic:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px"/>', obj.profile_pic.url)
        return "No Image"

    profile_picture_preview.short_description = "Profile Picture"  # Set column title in admin panel


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_location', 'preferred_education', 'preferred_age_range')
    list_filter = ('preferred_location', 'preferred_education')
    search_fields = ('user__username', 'preferred_location', 'preferred_education')
    ordering = ('user',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Preferences', {
            'fields': ('user', 'preferred_height_min', 'preferred_height_max', 
                       'preferred_age_min', 'preferred_age_max', 
                       'preferred_weight_min', 'preferred_weight_max', 
                       'preferred_education', 'preferred_location')
        }),
        ('Meta Information', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def preferred_age_range(self, obj):
        """Shows the preferred age range as 'min - max'."""
        return f"{obj.preferred_age_min} - {obj.preferred_age_max}" if obj.preferred_age_min and obj.preferred_age_max else "Not Set"

    preferred_age_range.short_description = "Preferred Age Range"

