from django.db import models
from django.contrib.auth.models import User

def profile_created_by_choices():
    """Returns choices for who created the profile."""
    return [
        ("self", "Self"),
        ("parent", "Parent"),
        ("sibling", "Sibling"),
        ("relative", "Relative"),
        ("friend", "Friend"),
    ]

def gender_choices():
    """Returns gender choices."""
    return [("male", "Male"), ("female", "Female")]

class BaseModel(models.Model):
    """Abstract model to add common fields across models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(BaseModel):
    """Model for storing user profile information."""

    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    created_by    = models.CharField(max_length=10, choices=profile_created_by_choices())
    gender        = models.CharField(max_length=6, choices=gender_choices())
    name          = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email         = models.EmailField(unique=True)
    height        = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # make nullable  # e.g., 175.5 cm
    age           = models.PositiveIntegerField()
    weight        = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    education     = models.CharField(max_length=255)
    country       = models.CharField(max_length=100)
    address       = models.TextField()
    phone_number  = models.CharField(max_length=20, unique=True)
    hide_phone_number = models.BooleanField(default=True)
    language      = models.CharField(max_length=100)
    religion      = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserPreference(BaseModel):
    """Model for storing user’s preferred partner criteria."""

    user                 = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    email                = models.EmailField(null=True, blank=True)
    preferred_height_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    preferred_height_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    preferred_age_min    = models.PositiveIntegerField(null=True, blank=True)
    preferred_age_max    = models.PositiveIntegerField(null=True, blank=True)
    preferred_weight_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    preferred_weight_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    preferred_education  = models.CharField(max_length=255, null=True, blank=True)
    preferred_location   = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"
