from django.urls import path
from .views import user_profile_list, user_profile_detail, user_preferences, user_registration

urlpatterns = [
    path('api/register/', user_registration, name='user-registration'),
    path('profiles/', user_profile_list, name='user-profile-list'),
    path('profiles/<int:pk>/', user_profile_detail, name='user-profile-detail'),
    path('preferences/', user_preferences, name='user-preferences'),
]
