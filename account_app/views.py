from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import MatchHistory, UserProfile, UserPreference
from .serializers import UserProfileSerializer, UserPreferenceSerializer, LastJoinedUserSerializer, UserProfileRegistrationSerializer, Explore_UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import LoginSerializer
from django.contrib.auth.models import User
from math import radians, sin, cos, sqrt, atan2
from .serializers import get_last_joined_user
from geopy.distance import geodesic


@swagger_auto_schema(method="post", request_body=LoginSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

@swagger_auto_schema(
    method='post', 
    request_body=Explore_UserSerializer, 
    responses={201: openapi.Response('User created', Explore_UserSerializer)}
)
@api_view(['POST'])
def find_matches(request):
    user_profile = request.user.userprofile
    
    max_distance = float(request.GET.get("radius", 50))

    # Get all other user profiles
    users = UserProfile.objects.exclude(user=request.user) 
    matched_users = []

    for u in users:
        if u.latitude and u.longitude:
            distance = calculate_distance(user_profile.latitude, user_profile.longitude, u.latitude, u.longitude)
            
            if distance <= max_distance:
                matched_users.append(u)
    
    serializer = UserProfileSerializer(matched_users, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post', 
    request_body=Explore_UserSerializer, 
    responses={201: openapi.Response('User created', Explore_UserSerializer)}
)
@api_view(['POST'])
def start_matching(request):
    # Extract latitude and longitude from the request data
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if not latitude or not longitude:
        return Response({"error": "Latitude and Longitude are required."}, status=400)

    # Create a reference location (tuple of latitude and longitude)
    reference_location = (latitude, longitude)

    # Get all users to check distance (you can filter based on other criteria if needed)
    users = User.objects.all()

    # Create a list of serialized users with distance info
    serializer = Explore_UserSerializer(users, many=True, context={'reference_location': reference_location})
    
    # Filter the users by distance (e.g., users within 10km radius)
    matched_users = [user for user in serializer.data if user.get('distance') <= 10]  # 10km radius
    
    return Response(matched_users)



@swagger_auto_schema(
    method='post', 
    request_body=UserProfileRegistrationSerializer, 
    responses={201: openapi.Response('User created', UserProfileRegistrationSerializer)}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserProfileRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save() 
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Return the tokens in the response
            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_201_CREATED)

        # If serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile List (GET, POST)
@swagger_auto_schema(
    method='get', 
    responses={200: UserProfileSerializer(many=True)}, 
    operation_description="Get all user profiles"
)
@swagger_auto_schema(
    method='post', 
    request_body=UserProfileSerializer, 
    responses={201: UserProfileSerializer},
    operation_description="Create a new user profile"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile_list(request):
    if request.method == 'GET':
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile Detail (GET, PUT, DELETE)
@swagger_auto_schema(
    method='get', 
    responses={200: UserProfileSerializer},
    operation_description="Retrieve a single user profile"
)
@swagger_auto_schema(
    method='put', 
    request_body=UserProfileSerializer,
    responses={200: UserProfileSerializer},
    operation_description="Update a user profile"
)
@swagger_auto_schema(
    method='delete', 
    responses={204: 'Profile deleted'},
    operation_description="Delete a user profile"
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_profile_detail(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response({'message': 'Profile deleted'}, status=status.HTTP_204_NO_CONTENT)


# User Preferences (GET, PUT)
@swagger_auto_schema(
    method='get', 
    responses={200: UserPreferenceSerializer}, 
    operation_description="Get user preferences"
)
@swagger_auto_schema(
    method='put', 
    request_body=UserPreferenceSerializer, 
    responses={200: UserPreferenceSerializer}, 
    operation_description="Update user preferences"
)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    preferences, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = UserPreferenceSerializer(preferences)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserPreferenceSerializer(preferences, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="get", responses={200: Explore_UserSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def explore_other_users(request):
    """Returns a list of all users (including full profile) except the logged-in user."""
    users = User.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    serializer = Explore_UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get', 
    responses={200: LastJoinedUserSerializer},
    operation_description="Retrieve a single user profile"
)
@api_view(['GET'])
def last_joined_user_view(request):
    """Function-based view to get the last joined user."""
    try:
        # Fetch and return the last joined user data
        last_user_data = get_last_joined_user()
        return Response(last_user_data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "No users found."}, status=status.HTTP_404_NOT_FOUND)
    
    

def calculate_match_percentage(user_profile, other_user_profile, user_preferences):
    match_score = 0
    total_score = 0

    # Compare Age
    if user_preferences.preferred_age_min and user_preferences.preferred_age_max:
        if user_preferences.preferred_age_min <= other_user_profile.age <= user_preferences.preferred_age_max:
            match_score += 1
        total_score += 1

    # Compare Height
    if user_preferences.preferred_height_min and user_preferences.preferred_height_max:
        if user_preferences.preferred_height_min <= other_user_profile.height <= user_preferences.preferred_height_max:
            match_score += 1
        total_score += 1

    # Compare Weight
    if user_preferences.preferred_weight_min and user_preferences.preferred_weight_max:
        if user_preferences.preferred_weight_min <= other_user_profile.weight <= user_preferences.preferred_weight_max:
            match_score += 1
        total_score += 1

    # Compare Location (you can calculate distance if latitude/longitude is set)
    if user_profile.latitude and user_profile.longitude and other_user_profile.latitude and other_user_profile.longitude:
        distance = geodesic(
            (user_profile.latitude, user_profile.longitude),
            (other_user_profile.latitude, other_user_profile.longitude)
        ).km
        if distance <= 50:  # 50 km as a threshold for matching location
            match_score += 1
        total_score += 1

    # Normalize and calculate match percentage
    if total_score > 0:
        match_percentage = (match_score / total_score) * 100
    else:
        match_percentage = 0

    return match_percentage


@api_view(['GET'])
def find_matches_allDetails(request):
    """
    Find matches for the logged-in user by comparing their profile and preferences with other users.
    """
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_preferences = UserPreference.objects.get(user=user)

    # Get all other users' profiles
    other_users_profiles = UserProfile.objects.exclude(user=user)

    matches = []

    # Compare each user to the logged-in user
    for other_user_profile in other_users_profiles:
        match_percentage = calculate_match_percentage(user_profile, other_user_profile, user_preferences)

        # If match is above a certain threshold, add to matches
        if match_percentage > 0:  # You can define a minimum match percentage if needed
            matches.append({
                "user_id": other_user_profile.user.id,
                "username": other_user_profile.user.username,
                "match_percentage": match_percentage,
                "profile_pic": other_user_profile.profile_pic.url if other_user_profile.profile_pic else None,
            })

    # Return the list of matches
    return Response({"matches": matches})


from .serializers import PreferredEducationSerializer, PreferredLocationSerializer


@swagger_auto_schema(
    method='PUT', 
    responses={200: PreferredEducationSerializer},
    operation_description="Retrieve a single user profile"
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_preferred_education(request):
    try:
        user_preference = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        return Response({"detail": "User preferences not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PreferredEducationSerializer(user_preference, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT', 
    responses={200: PreferredLocationSerializer},
    operation_description="Retrieve a single user profile"
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_preferred_location(request):
    try:
        user_preference = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        return Response({"detail": "User preferences not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PreferredLocationSerializer(user_preference, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Revoke refresh token to ensure it's no longer valid
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()  # This will blacklist the token (assuming the blacklist app is enabled)

        return Response({"detail": "Successfully logged out"}, status=200)
    except Exception as e:
        return Response({"detail": f"Error logging out: {str(e)}"}, status=400)
    

@api_view(['GET'])
@permission_classes(IsAuthenticated)
def get_matches_history(request):
    # Get the logged-in user's matches history
    matches = MatchHistory.objects.filter(user=request.user).select_related('matched_user')

    match_history = []
    for match in matches:
        matched_user_profile = UserProfile.objects.get(user=match.matched_user)
        match_history.append({
            "matched_user": match.matched_user.username,
            "match_percentage": match.match_percentage,
            "profile_picture": matched_user_profile.profile_picture.url if matched_user_profile.profile_picture else None,
            "created_at": match.created_at
        })

    return Response(match_history, status=status.HTTP_200_OK)
