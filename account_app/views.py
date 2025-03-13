from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile, UserPreference
from .serializers import UserProfileSerializer, UserPreferenceSerializer, UserProfileRegistrationSerializer, Explore_UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import LoginSerializer
from django.contrib.auth.models import User

@swagger_auto_schema(method="post", request_body=LoginSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# User Registration (POST)
@swagger_auto_schema(
    method='post', 
    request_body=UserProfileRegistrationSerializer, 
    responses={201: openapi.Response('User created', UserProfileRegistrationSerializer)}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method == 'POST':
        # Deserialize data using the registration serializer
        serializer = UserProfileRegistrationSerializer(data=request.data)
        
        # If the serializer is valid, save the user, profile, and preference
        if serializer.is_valid():
            user = serializer.save()  # This will create the profile and preference
            
            # Generate JWT tokens for the user
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