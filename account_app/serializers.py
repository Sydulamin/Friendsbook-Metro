from rest_framework import serializers
from .models import UserProfile, UserPreference
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # Include all fields

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'


class UserProfileRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    created_by = serializers.ChoiceField(choices=[('self', 'Self'), ('parent', 'Parent'), ('sibling', 'Sibling'), ('relative', 'Relative'), ('friend', 'Friend')])
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')])
    name = serializers.CharField(max_length=255)
    date_of_birth = serializers.DateField()
    email = serializers.EmailField()
    height = serializers.DecimalField(max_digits=5, decimal_places=2)
    age = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    education = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    hide_phone_number = serializers.BooleanField(default=True)
    language = serializers.CharField(max_length=100)
    religion = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 
                  'created_by', 'gender', 'name', 'date_of_birth', 'height', 
                  'age', 'weight', 'education', 'country', 'address', 
                  'phone_number', 'hide_phone_number', 'language', 'religion']

    def create(self, validated_data):
        user_data = {key: validated_data.pop(key) for key in ['username', 'email', 'password', 'first_name', 'last_name']}
        user = User.objects.create_user(**user_data)

        # Create profile
        profile_data = {key: validated_data.pop(key) for key in validated_data if key not in ['height', 'age', 'weight', 'education', 'country', 'address', 'phone_number', 'hide_phone_number', 'language', 'religion']}
        profile = UserProfile.objects.create(user=user, **profile_data)

        # Create preferences (optional but if you want to create them too)
        preferences_data = {key: validated_data.pop(key) for key in ['preferred_height_min', 'preferred_height_max', 'preferred_age_min', 'preferred_age_max', 'preferred_weight_min', 'preferred_weight_max', 'preferred_education', 'preferred_location']}
        preferences = UserPreference.objects.create(user=user, **preferences_data)

        return user