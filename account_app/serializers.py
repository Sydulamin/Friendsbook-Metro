from datetime import date
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

    # UserProfile fields
    created_by = serializers.ChoiceField(choices=[("self", "Self"), ("parent", "Parent"), ("sibling", "Sibling"), ("relative", "Relative"), ("friend", "Friend")])
    gender = serializers.ChoiceField(choices=[("male", "Male"), ("female", "Female")])
    name = serializers.CharField(max_length=255)
    date_of_birth = serializers.DateField()
    height = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    education = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=100)
    address = serializers.CharField()
    phone_number = serializers.CharField(max_length=20)
    hide_phone_number = serializers.BooleanField(default=True)
    language = serializers.CharField(max_length=100)
    religion = serializers.CharField(max_length=100)

    # UserPreference fields
    preferred_height_min = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    preferred_height_max = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    preferred_age_min = serializers.IntegerField(required=False)
    preferred_age_max = serializers.IntegerField(required=False)
    preferred_weight_min = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    preferred_weight_max = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    preferred_education = serializers.CharField(max_length=255, required=False)
    preferred_location = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'created_by', 'gender', 'name', 'date_of_birth', 'height', 'weight',
            'education', 'country', 'address', 'phone_number', 'hide_phone_number', 'language', 'religion',
            'preferred_height_min', 'preferred_height_max', 'preferred_age_min', 'preferred_age_max',
            'preferred_weight_min', 'preferred_weight_max', 'preferred_education', 'preferred_location'
        ]

    def create(self, validated_data):
        # Extract user-related data
        password = validated_data.pop('password')
        user_data = {key: validated_data[key] for key in ['username', 'email', 'first_name', 'last_name']}
        user = User.objects.create(**user_data)
        
        # Set the password after user creation
        user.set_password(password)
        user.save()

        # Calculate age from date_of_birth
        date_of_birth = validated_data.get('date_of_birth')
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

        # Create UserProfile data
        profile_data = {key: validated_data[key] for key in ['created_by', 'gender', 'name', 'date_of_birth', 'height', 'weight', 'education', 'country', 'address', 'phone_number', 'hide_phone_number', 'language', 'religion']}
        profile_data['user'] = user
        profile_data['age'] = age  # Set the calculated age
        profile_data['email'] = validated_data['email']  # Add email to the profile
        profile = UserProfile.objects.create(**profile_data)

        # Create UserPreference data
        preference_data = {key: validated_data[key] for key in ['preferred_height_min', 'preferred_height_max', 'preferred_age_min', 'preferred_age_max', 'preferred_weight_min', 'preferred_weight_max', 'preferred_education', 'preferred_location']}
        preference_data['user'] = user
        preference_data['email'] = validated_data['email']  # Add email to preferences
        preference = UserPreference.objects.create(**preference_data)

        return user