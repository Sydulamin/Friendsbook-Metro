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

# <------------------------------------- Registration Area ------------------------------------->    
   
class UserProfileRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_pic = serializers.ImageField(source="profile_picture", required=False)
    

    # UserProfile fields
    created_by = serializers.ChoiceField(choices=[("self", "Self"), ("parent", "Parent"), ("sibling", "Sibling"), ("relative", "Relative"), ("friend", "Friend")])
    gender = serializers.ChoiceField(choices=[("male", "Male"), ("female", "Female")])
    name = serializers.CharField(max_length=255)
    date_of_birth = serializers.DateField()
    height = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    education = serializers.CharField(max_length=255, required=False)
    country = serializers.CharField(max_length=100, required=False)
    address = serializers.CharField(required=False)
    phone_number = serializers.CharField(max_length=20, required=False)
    hide_phone_number = serializers.BooleanField(default=True)
    language = serializers.CharField(max_length=100, required=False)
    religion = serializers.CharField(max_length=100 , required=False)

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
            'username', 'email', 'password', 'first_name', 'last_name','profile_pic',
            'created_by', 'gender', 'name', 'date_of_birth', 'height', 'weight',
            'education', 'country', 'address', 'phone_number', 'hide_phone_number', 'language', 'religion',
            'preferred_height_min', 'preferred_height_max', 'preferred_age_min', 'preferred_age_max',
            'preferred_weight_min', 'preferred_weight_max', 'preferred_education', 'preferred_location'
        ]

    def create(self, validated_data):
        profile_pic_data = validated_data.pop('profile_pic', None)
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

        if profile_pic_data:
            format, imgstr = profile_pic_data.split(';base64,')  # Extract the format and base64 string
            ext = format.split('/')[1]  # Extract the file extension (e.g., png, jpeg)
            image_data = ContentFile(base64.b64decode(imgstr), name="profile_pic." + ext)
            validated_data['profile_picture'] = image_data 
        
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
    
# <------------------------------------- Login Area ------------------------------------->    
    
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Check if user exists with this email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        # Authenticate using email
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


# <------------------------------------- Explore Area ------------------------------------->
class Explore_UserSerializer(serializers.ModelSerializer):
    userprofile = serializers.SerializerMethodField()  # Get full user profile data

    class Meta:
        model = User
        fields = ["username", "userprofile"]  # Include full UserProfile inside

    def get_userprofile(self, obj):
        """Fetch all user profile data dynamically."""
        user_profile = UserProfile.objects.get(user=obj)
        return {
            "id": user_profile.id,
            "country": user_profile.country,
            "profile_picture": user_profile.profile_picture.url if user_profile.profile_picture else None,
            "bio": user_profile.bio,
            "phone_number": user_profile.phone_number,
            "date_of_birth": user_profile.date_of_birth,
            "gender": user_profile.gender,
            "address": user_profile.address,
            "city": user_profile.city,
            "zip_code": user_profile.zip_code,
            "created_at": user_profile.created_at,
        }
